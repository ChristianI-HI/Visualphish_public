import subprocess
import os
# import webcolors
import multiprocessing
import csv
from pathlib import Path
import os
import sys
import json
import shutil
import glob
import argparse

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand_name", type=str, default = "yahoo", help="Brand Name")
    parser.add_argument("--background_color", type=int, default=1, help="Background Color")
    return parser.parse_args()


# Define a function to run a command using subprocess.run()
def run_command(command):
    print(command)
    try:
        result = subprocess.run(command)
    except:
        print("Error in command: ", command)

def get_ttf_file_list(path: str):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(".ttf") or file.endswith(".TTF")
    ]

def get_json_file_list(path: str):
    """Get a list of all .json files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(".json")
    ]

def get_ttf_files(directory_path):
    file_paths = glob.glob(directory_path + "/*.ttf")
    return file_paths

def get_folder_list(directory):
    """Get a list of all folders in a directory"""
    return [
        os.path.join(directory, folder)
        for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]

def appendToCSV(row, filepath, verbose = True):
	"""
	Appends a csv 
	"""
	if verbose == True: print(row, 'appending into', filepath, '.........')
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	if verbose == True: print('Appended')

def make_directory_tree(pathname):
	"""
	Creats  hierarchical paths
	"""
	path = Path(pathname)
	path.mkdir(parents = True, exist_ok = True)

import shutil
def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print("File copied successfully!")
    except IOError as e:
        print(f"An error occurred while copying the file: {e}")

def check_file_exists(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False


if __name__ == "__main__":

    args = config()
    
    BRAND_NAME = args.brand_name 
    OUTPUT_DIR = '../../generated_fonts/' + BRAND_NAME + "-noise/"
    INPUT_FILE = '../../inputs/' + BRAND_NAME + "/input.txt"
    COLOR_INPUT_FOLDER = "../../inputs/" + BRAND_NAME + "/color_schemes/"

    COLOR_VARS = get_json_file_list(COLOR_INPUT_FOLDER)
    STROKE_WIDTH_VARS = ['3', '4']
    STROKE_FILL_COLORS_VARS = ["#410093", "#5b00ce", "#b87fff", "#420b88"]
    CHAR_SPACE_VARS = ['-11','-9','9', '11']
    ALIGNMENT_VARS = ['0']
    BLUR_VARS = ['1', '2', '3']
    
    BACKGROUND_VAR = args.background_color
    MARGIN = 20

    c = 0
    GLOBAL_FONT_DIR = "/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/font_generation/fonts/"
    
    FONT_TYPE_PATHS = ["custom-fonts", "google-open-source-fonts"]
    nf_done_fonts = 0
    
    for font_type_path in FONT_TYPE_PATHS:
        CURRENT_FONT_DIR = os.path.join(GLOBAL_FONT_DIR, font_type_path)
        FONT_FOLDERS = get_folder_list(CURRENT_FONT_DIR)

        make_directory_tree(OUTPUT_DIR + font_type_path + "/")

        for FONT_DIR in FONT_FOLDERS:
            fonts = get_ttf_file_list(FONT_DIR)
            final_fonts = get_ttf_files(FONT_DIR)

            print("Total Number of done fonts: ", nf_done_fonts)

            for font_path in fonts:
                font_name = font_path.split("/")[-1]
                check_path = FONT_DIR + "/" + font_name

                if check_file_exists(check_path) == False:
                    copy_file(font_path, check_path)
            
            final_fonts = get_ttf_files(FONT_DIR)
            len_fonts = len(final_fonts)

            FONT_OUTPUT_DIR = OUTPUT_DIR + font_type_path + "/" + FONT_DIR.split("/")[-1] + "/"
            
            make_directory_tree(FONT_OUTPUT_DIR)

            appendToCSV([FONT_DIR.split("/")[-1], len_fonts], OUTPUT_DIR + font_type_path + "/" + "check_fonts.csv", verbose = True)
            commands = []

            for COLOR in COLOR_VARS:
                for STROKE in STROKE_WIDTH_VARS:
                    for STROKE_FILL_COLOR in STROKE_FILL_COLORS_VARS:
                        for CHAR_SPACE in CHAR_SPACE_VARS:
                            for ALIGNMENT in ALIGNMENT_VARS:
                                for BLUR in BLUR_VARS:
                                    commands.append(['python3.7', 'run.py',
                                                    '--input_file', INPUT_FILE,
                                                    '--text_color', COLOR,
                                                    '--count', str(len_fonts), 
                                                    '--font_dir', FONT_DIR,
                                                    '--output_dir', FONT_OUTPUT_DIR,
                                                    '--name_format', str(3),
                                                    '--margin', str(MARGIN),
                                                    '--blur', str(BLUR),
                                                    '--stroke_width', str(STROKE),
                                                    '--stroke_fill', str(STROKE_FILL_COLOR), 
                                                    '--format', str(256),
                                                    '--background', str(BACKGROUND_VAR),
                                                    "--alignment", str(ALIGNMENT),
                                                    "--character_spacing", str(CHAR_SPACE)
                                                    ])
                                    c += 1

            # Create a multiprocessing pool with the number of processes you want to use
            pool = multiprocessing.Pool(processes = 200)

            # Run each command in a separate process using the pool.map() method
            pool.map(run_command, commands)

            # Close the pool to prevent any more tasks from being submitted to it
            pool.close()

            # Wait for all processes to finish
            pool.join()

            nf_done_fonts += len_fonts