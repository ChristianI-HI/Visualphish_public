import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '7'

from PhishIntention.phishintention.phishintention_main import test
from PhishIntention.phishintention.phishintention_config import load_config
import os
import shutil
import sys

import sys
sys.path.append("../../")

from paths import *
import read_write_fns
import argparse

def get_param_file():
    """Take in the file from the command line"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--brand_name', type=str, default= "instagram", help='Testing on which dataset')
    parser.add_argument('--k', type=int, default= 200, help='Number of Top k logos to be selected')
    parser.add_argument('--device', type=str, default= "cuda", help='The device to run the model on')
    args = parser.parse_args()
    return args.brand_name, args.k, args.device

if __name__ == "__main__":
    BRAND_NAME, top_k, device = get_param_file()

    cfg_path = None 
    AWL_MODEL, CRP_CLASSIFIER, CRP_LOCATOR_MODEL, SIAMESE_MODEL, OCR_MODEL, SIAMESE_THRE, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH = load_config(cfg_path, device)

    url = open(f"{PROJECT_PATH}/data/input/{BRAND_NAME}/info.txt").read().strip()
    SCREENSHOT_FOLDER = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{top_k}/all/"
    SUCCESS_OUTPUT_FOLDER = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{top_k}/success/"
    FAILURE_OUTPUT_FOLDER = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{top_k}/failure/"

    read_write_fns.make_directory_tree(SUCCESS_OUTPUT_FOLDER)
    read_write_fns.make_directory_tree(FAILURE_OUTPUT_FOLDER)

    files_list = read_write_fns.get_files_with_string_in_name_deep(SCREENSHOT_FOLDER, ".png")

    none_cases_count = 0
    total, success = 0, 0

    all_siam_confs, successes, fails = [], [], []

    for screenshot_path in files_list:
        filename = os.path.basename(screenshot_path)
        phish_category, _, _, siamese_conf, _, _, _, _, _ = test(url, screenshot_path, AWL_MODEL, CRP_CLASSIFIER, CRP_LOCATOR_MODEL, SIAMESE_MODEL, OCR_MODEL, SIAMESE_THRE, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH)
        
        if phish_category == 0:
            shutil.copyfile(screenshot_path, f"{SUCCESS_OUTPUT_FOLDER}/{filename[:-4]}_{siamese_conf}.png")
            successes.append((screenshot_path, siamese_conf))
            success += 1
        else:
            shutil.copyfile(screenshot_path, f"{FAILURE_OUTPUT_FOLDER}/{filename[:-4]}_{siamese_conf}.png")
            fails.append((screenshot_path, siamese_conf))

        if siamese_conf:
            siamese_conf = round(siamese_conf, 3)
            all_siam_confs.append(siamese_conf)
        else:
            none_cases_count += 1

        total += 1

    avg_conf = sum(all_siam_confs) / len(all_siam_confs)
    print("Average Confidence: ", avg_conf)

    results = {
        "total": total,
        "success": success,
        "fail": total - success,
        "avg_conf": avg_conf,
        "none_cases": none_cases_count
    }

    # Dump the information to a file
    read_write_fns.dumpJsonFile(results, f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{top_k}/results.json", )
