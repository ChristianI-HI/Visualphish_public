import os
from PhishIntention.phishintention.phishintention_config import load_config
from PhishIntention.phishintention.src.OCR_siamese_utils.inference import siamese_inference_logo
from PhishIntention.phishintention.src.OCR_siamese_utils.inference import  get_OCR_embed

import os
import sys
import argparse
from PIL import Image

import sys
sys.path.append("../../")

from paths import *
import read_write_fns
import numpy as np

def get_param_file():
    """Take in the file from the command line"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--brand_name', type=str, default= "instagram", help='Testing on which dataset')
    parser.add_argument('--threshold', type=float, default= 0.87, help='Threshold for the siamese model')
    parser.add_argument('--k', type=int, default= 200, help='Number of Top k logos to be selected')
    parser.add_argument('--device', type=str, default= "cuda", choices = ["cuda", "cpu"], help='the device choices')
    parser.add_argument('--logo_level_eval', type=bool, default= True, help='Whether to evaluate the logos on a logo level')
    args = parser.parse_args()
    return  args.threshold, args.k, args.brand_name, args.device, args.logo_level_eval

def get_file_list(directory_path):
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".png"):
                file_list.append(os.path.join(root, file))
    return file_list

def cosine_similarity(x1, x2):
    '''Cosine similarity between two vectors of type numpy.ndarray'''
    dot_product1 = np.dot(x1, x2.T)
    # print("Dot Product 1", dot_product1) 
    # dot_product = np.dot(x1, x2)
    # print("Dot Product", dot_product)
    
    norm_x1 = np.linalg.norm(x1)
    norm_x2 = np.linalg.norm(x2)
    
    # print("Norms",norm_x1, norm_x2)
    product_norms = norm_x1 * norm_x2
    # print("Product Norms", product_norms)
    cos_sim = dot_product1 / product_norms
    # print("Cosine Similarity", cos_sim)
    return cos_sim

def convert_tensor_to_numpy(x):
    return x.cpu().numpy()

def resize_image(image1_path, image2_path):
    """
    Resizes the image
    """
    im1 = Image.open(image1_path)
    width1, height1 = im1.size
    im2 = Image.open(image2_path)
    im2.thumbnail((width1, height1), Image.ANTIALIAS)
    return im2

def make_buckets(buc_vals, arr = [(str, float)]):
    """
    Given a list of bucket values, and a list of tuples, bucket the values into sets and store the 
    """
    buc_vals.sort(reverse = True)
    bucket_keys = range(len((buc_vals)))
    buckets = {}

    for key in bucket_keys:
        buckets[key] = []

    j = 0
    for i in range(len(arr)):
        val = arr[i][1]
        filepath = arr[i][0]
        if val <= buc_vals[j]:
            if j < len(buc_vals) - 1:
                if val > buc_vals[j+1]:
                    buckets[j].append((val, filepath))
                else:
                    j += 1
    
    return buckets


if __name__ == "__main__":
    THRESHOLD, top_k, BRAND_NAME, device, LOGO_LEVEL_EVAL = get_param_file()

    # Load the models
    cfg_path, device = None, 'cuda' 
    AWL_MODEL, CRP_CLASSIFIER, CRP_LOCATOR_MODEL, SIAMESE_MODEL, OCR_MODEL, SIAMESE_THRE, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH = load_config(cfg_path, device)

    BRAND_NAME = BRAND_NAME.lower()
    
    url = open(f"{PROJECT_PATH}/data/input/{BRAND_NAME}/info.txt").read().strip()
    ATTACK_FOLDER = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/logos/"
    TARGET_FOLDER  = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/top_{top_k}_logos/"

    read_write_fns.make_directory_tree(TARGET_FOLDER)

    total, success = 0, 0

    # Get the original image and its OCR embedding
    orig_img_path = f"{PROJECT_PATH}/data/input/instagram/orig_logo.png"
    orig_ocr_embed = get_OCR_embed(orig_img_path, OCR_MODEL, imshow=False, title="OCR embedding", grayscale=False).cpu().numpy()

    files_list = read_write_fns.get_files_with_string_in_name_deep(ATTACK_FOLDER, ".png")
    
    all_ocr_sims = []
    ocr_sims = []
    num_error_files = 0

    for filepath_no, filepath in enumerate(files_list):
        filename = filepath.split("/")[-1]
        cand_font_img = Image.open(filepath)

        cand_font_ocr_embed = get_OCR_embed(cand_font_img, OCR_MODEL, imshow=False, title="OCR embedding", grayscale=False).cpu().numpy()

        sim = cosine_similarity(cand_font_ocr_embed, orig_ocr_embed)
        print("Cosine Similarity: ", sim, filepath_no, filepath)
        
        img_index = int(filename.split("_")[0])

        if sim < THRESHOLD:
            ocr_sims.append([sim[0][0], img_index, filepath, cand_font_img])

        all_ocr_sims.append([sim[0][0], img_index, filepath])

        if filepath_no % 500 == 0:
            print(f"Processed {filepath_no} files")

    ocr_sims = sorted(ocr_sims, key = lambda x: x[0], reverse = True)
    top_k_sims = ocr_sims[:top_k]

    total, success = 0, 0
    print("---- OCR Similarity Calculated ----")

    filepath = f"{TARGET_FOLDER}/all_ocr_sims.csv"
    read_write_fns.dumpCSVfile(all_ocr_sims, filepath, verbose = True)


    if LOGO_LEVEL_EVAL:
        print("---- Evaluating on Logo Level ----")

    for k_info in top_k_sims:
        img_index, ocr_siam_info, cand_font_img = k_info[1], k_info[0], k_info[3]
    
        filename = k_info[2].split("/")[-1][:-4] + f"_{k_info[0]}.png"
        candidate_img_path = f"{TARGET_FOLDER}/{filename}"
        cand_font_img.save(candidate_img_path)

        if LOGO_LEVEL_EVAL:
            # Get the logo phishintention similarity  
            domain_map = read_write_fns.loadPickleFile(DOMAIN_MAP_PATH)
            _, _, logo_siam_conf = siamese_inference_logo(SIAMESE_MODEL, OCR_MODEL, domain_map, LOGO_FEATS, LOGO_FILES, candidate_img_path, t_s=0.87, grayscale=False)

            # Round the confidence to 3 decimal places
            logo_siam_conf = round(logo_siam_conf, 3)
            
            if logo_siam_conf < 0.87:
                success += 1

        if LOGO_LEVEL_EVAL:
            print(f"Total: {total}, Success: {success}")
        

        total += 1

