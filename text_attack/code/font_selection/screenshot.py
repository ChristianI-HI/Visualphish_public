import numpy as np
from PIL import Image, ImageOps, ImageDraw
import argparse

import sys
sys.path.append("../../")

from paths import *
import read_write_fns


def get_param_file():
    """Take in the file from the command line"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--brand_name', type=str, default= "instagram", help='Testing on which dataset')
    parser.add_argument('--k', type=int, default= 200, help='Number of Top k logos to be selected')
    args = parser.parse_args()
    return args.brand_name, args.k

def find_coordinates(subimage_path, fullimage_path):
    """
    Returns the coordinates of the subimage in the full image
    """
    here = Image.open(subimage_path)
    big  = Image.open(fullimage_path)

    herear = np.asarray(here)
    bigar  = np.asarray(big)

    hereary, herearx = herear.shape[:2]
    bigary,  bigarx  = bigar.shape[:2]

    stopx = bigarx - herearx + 1
    stopy = bigary - hereary + 1

    x1 = None
    y1 = None

    for x in range(0, stopx):
        for y in range(0, stopy):
            x2 = x + herearx
            y2 = y + hereary
            pic = bigar[y:y2, x:x2]
            test = (pic == herear)
            
            if test.all():
                print(x,y)
                x1, y1 = x, y
    return x1, y1

def paste_image(image1, image2, coordinates, output_image_path):
    """
    Paste Image 2 on Image 1 at the coordinates
    """
    image1.paste(image2, coordinates)
    image1.save(output_image_path)

def get_image_shape(image_path):
    """
    Returns the shape of the image
    """
    image = Image.open(image_path)
    return image.size

def draw_patch_over_image(image, coordinates, dimensions, color = (255, 255, 255)):
    """
    Draws a patch over the image
    """
    draw = ImageDraw.Draw(image)
    (x, y) = coordinates
    (w, h) = dimensions
    shape = [(x, y), (x + w, y + h)]
    draw.rectangle(shape, fill= color, outline=color)
    return draw

if __name__ == "__main__":
    BRAND_NAME, TOP_K = get_param_file()

    BRAND_PARAMS_FILE = f"{PROJECT_PATH}/data/input/brand_params.json"
    brand_params = read_write_fns.loadJsonFile(BRAND_PARAMS_FILE)

    ATTACK_FOLDER_PATH = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/top_{TOP_K}_logos/"
    SCREENSHOT_PATH = f"{PROJECT_PATH}/data/input/{BRAND_NAME}/screenshot.png"
    ORIG_FONT_PATH = f"{PROJECT_PATH}/data/input/{BRAND_NAME}/orig_logo.png"
    OUTPUT_IMAGE_FOLDER = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{TOP_K}/all/"

    # Brand Specific Parameters
    screenshot_name = brand_params[BRAND_NAME]["screenshot"]
    change_x, change_y = brand_params[BRAND_NAME]["change_x"], brand_params[BRAND_NAME]["change_y"]
    BRAND_TYPE, PATCH_COLOR = brand_params[BRAND_NAME]["brand_type"], brand_params[BRAND_NAME]["patch_color"]

    # Find where the original logo is in the screenshot
    orig_font_shape = get_image_shape(ORIG_FONT_PATH)
    w, h = orig_font_shape
    (x, y) = find_coordinates(ORIG_FONT_PATH, SCREENSHOT_PATH)

    num_total_imgs, num_error_imgs = 0, 0
    global_png_paths = read_write_fns.get_files_with_string_in_name_deep(ATTACK_FOLDER_PATH, ".png")
    
    for ATTACK_FONT_PATH in global_png_paths:
        filename = ATTACK_FONT_PATH.split("/")[-1][:-4]
        attach_font_image = Image.open(ATTACK_FONT_PATH)

        OUTPUT_BUCKET_IMAGE_PATH = f"{OUTPUT_IMAGE_FOLDER}/"
        read_write_fns.make_directory_tree(OUTPUT_BUCKET_IMAGE_PATH) 
        
        screenshot_image = Image.open(SCREENSHOT_PATH)
        _ = draw_patch_over_image(screenshot_image, (x, y), (w, h), color = (PATCH_COLOR[0], PATCH_COLOR[1], PATCH_COLOR[2]))

        paste_image(screenshot_image, attach_font_image, (x + change_x, y + change_y), f"{OUTPUT_BUCKET_IMAGE_PATH}/{filename}.png")
        num_total_imgs += 1

    print("Total error images: ", num_error_imgs)
    print("Total images: ", num_total_imgs)
    print("All images :", len(global_png_paths))