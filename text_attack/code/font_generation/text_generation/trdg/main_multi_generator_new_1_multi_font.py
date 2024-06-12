import subprocess
import os
import webcolors
import multiprocessing
import csv
from pathlib import Path
import os
import sys
import json
import shutil
import glob

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

    BRAND_NAME = "yahoo"

    # FONT_DIR = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/google-open-source-fonts/all_fonts/"
    OUTPUT_DIR = '../../generated_fonts/' + BRAND_NAME + "/"
    INPUT_FILE = '../../inputs/' + BRAND_NAME + "/"+ BRAND_NAME + ".txt"
    COLOR_INPUT_FILE = "../../inputs/" + BRAND_NAME + "/colors.json"

    # FONTS = ["spotify-font", "gotham-rounded", "montserrat", "arial", "helvetica", "helvetica-neue"]
    COLOR_VARS = [COLOR_INPUT_FILE]
    STROKE_WIDTH_VARS = ['0']
    STROKE_FILL_COLORS_VARS = ["#000000"]
    CHAR_SPACE_VARS = ['0']
    ALIGNMENT_VARS = ['0']

    MARGIN = 20

    c = 0

    # GLOBAL_FONT_DIR = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/"
    GLOBAL_FONT_DIR = "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/"
    FONT_TYPE_PATHS = ["custom-fonts", "google-open-source-fonts"]
    
    for COLOR in COLOR_VARS:
        for STROKE in STROKE_WIDTH_VARS:
            for STROKE_FILL_COLOR in STROKE_FILL_COLORS_VARS:
                for CHAR_SPACE in CHAR_SPACE_VARS:
                    for ALIGNMENT in ALIGNMENT_VARS:
                        commands.append(['python3', 'run.py',
                                        '--input_file', INPUT_FILE,
                                        '--text_color', COLOR,
                                        '--count', str(len_fonts), 
                                        '--font_dir', FONT_DIR,
                                        '--output_dir', FONT_OUTPUT_DIR,
                                        '--name_format', str(3),
                                        '--margin', str(MARGIN),
                                        '--stroke_width', str(STROKE),
                                        '--stroke_fill', str(STROKE_FILL_COLOR), 
                                        '--format', str(256),
                                        '--background', '1',
                                        "--alignment", str(ALIGNMENT),
                                        "--character_spacing", str(CHAR_SPACE)
                                        ])
                        c += 1

        # Create a multiprocessing pool with the number of processes you want to use
        pool = multiprocessing.Pool(processes = 50)

        # Run each command in a separate process using the pool.map() method
        pool.map(run_command, commands)

        # Close the pool to prevent any more tasks from being submitted to it
        pool.close()

        # Wait for all processes to finish
        pool.join()
