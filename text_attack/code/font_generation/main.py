import subprocess
import os
import multiprocessing
from pathlib import Path
import os
import sys
import json
import shutil
from PIL import Image
import font_gen_utils

sys.path.append('../..')
from paths import PROJECT_PATH
import read_write_fns 

import argparse

# Define a function to run a command using subprocess.run()
def run_command(command):
    result = subprocess.run(command)

def get_file_list(path: str, search_string : str = ".ttr"):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.lower().endswith(search_string)
    ]

def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print("File copied successfully!")
    except IOError as e:
        print(f"An error occurred while copying the file: {e}")


def get_params():
    """Take in the parameter filepath from terminal and parse it using argparse"""
    parser = argparse.ArgumentParser(description='Tokenize the data')
    parser.add_argument('--brand_name', type=str, default= "instagram", help='Filepath of the parameter file')
    args = parser.parse_args()
    return args.brand_name


if __name__ == "__main__":

    BRAND_NAME = get_params()

    ORIGINAL_FONT_PATH =  f"{PROJECT_PATH}/data/input/{BRAND_NAME}/orig_logo.png"
    GLOBAL_FONT_DIR = f"{PROJECT_PATH}/font_generation/fonts/"
    OUTPUT_DIR = f"{PROJECT_PATH}/data/output/{BRAND_NAME}/logos/"
    INPUT_FILE = f"{PROJECT_PATH}/data/input/{BRAND_NAME}/font_gen/logo_text.txt"
    COLOR_INPUT_FILE = f"{PROJECT_PATH}/data/input/{BRAND_NAME}/font_gen/colors.json"

    colors_file = json.load(open(COLOR_INPUT_FILE))

    background_color = font_gen_utils.get_bg_color(COLOR_INPUT_FILE, ORIGINAL_FONT_PATH)

    COLOR, STROKE, STROKE_FILL_COLOR, CHAR_SPACE, ALIGNMENT = COLOR_INPUT_FILE, '0', "#000000", '0', '0'
    c, MARGIN = 0, 20

    GLOBAL_FONT_DIR = f"{PROJECT_PATH}/data/fonts/"
    FONT_TYPE_PATHS = ["custom-fonts", "google-open-source-fonts"]

    run_command_str = f"{PROJECT_PATH}/code/font_generation/text_generation/trdg/run.py"

    for font_type_path in FONT_TYPE_PATHS:
        CURRENT_FONT_DIR = os.path.join(GLOBAL_FONT_DIR, font_type_path)
        FONT_FOLDERS = read_write_fns.get_folder_list(CURRENT_FONT_DIR)

        read_write_fns.make_directory_tree(f"{OUTPUT_DIR}/{font_type_path}/")

        commands = []

        for FONT_NO, FONT_DIR in enumerate(FONT_FOLDERS):

            fonts = read_write_fns.get_files_with_string_in_name_deep(FONT_DIR, ".ttf")

            for font_path in fonts:
                font_name = font_path.split("/")[-1]
                check_path = FONT_DIR + "/" + font_name

                if read_write_fns.check_file_exists(check_path) == False:
                    copy_file(font_path, check_path)
            
            len_fonts = len(fonts)

            FONT_OUTPUT_DIR = OUTPUT_DIR + font_type_path + "/" + FONT_DIR.split("/")[-1] + "/"

            print(FONT_OUTPUT_DIR)
            print(FONT_DIR)
            
            read_write_fns.make_directory_tree(FONT_OUTPUT_DIR)
            
            commands.append(['python3.7', run_command_str,
                            '--input_file', INPUT_FILE,
                            '--text_color', COLOR,
                            '--count', str(len_fonts), 
                            '--font_dir', FONT_DIR,
                            '--output_dir', FONT_OUTPUT_DIR,
                            '--name_format', str(4),
                            '--margin', str(MARGIN),
                            '--stroke_width', str(STROKE),
                            '--stroke_fill', str(STROKE_FILL_COLOR), 
                            '--format', str(256),
                            '--background', '5',
                            '--background_color', background_color,
                            "--alignment", str(ALIGNMENT),
                            "--character_spacing", str(CHAR_SPACE)
                            ])
        
            c += 1

            print("Number of Commands = ", len(commands))

            read_write_fns.appendToCSV([FONT_DIR.split("/")[-1], len_fonts], OUTPUT_DIR + font_type_path + "/" + "check_fonts.csv", verbose = True)
    
            if (FONT_NO % 25 == 0) and (FONT_NO != 0):
                pool = multiprocessing.Pool(processes = 100)
                pool.map(run_command, commands)
                pool.close()
                pool.join()
                commands = []
        
        pool = multiprocessing.Pool(processes = 100)
        pool.map(run_command, commands)
        pool.close()
        pool.join()
        commands = []
    

    filepaths = read_write_fns.get_files_with_string_in_name_deep(OUTPUT_DIR, ".jpg")
    
    print("Number of logos generated: ", len(filepaths))

    for filepath in filepaths:

        print(filepath)
        # Get the filename
        filename = filepath.split("/")[-1]
        folderpath = filepath.replace(filename, "")
        
        # Define the destination folder
        destination_filepath = f"{folderpath}/{filename[:-4]}.png"

        print(destination_filepath)
        
        # Create the folder if it does not exist
        font_gen_utils.resize_image_from_path(ORIGINAL_FONT_PATH, filepath, save_img_path = destination_filepath)

        # Delete the original file
        os.remove(filepath)
    
    png_filepaths = read_write_fns.get_files_with_string_in_name_deep(OUTPUT_DIR, ".png")
    
    print("Number of logos generated: ", len(png_filepaths))
                