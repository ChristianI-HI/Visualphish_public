import subprocess
import os

import multiprocessing
import csv
from pathlib import Path
import os
import sys
import json
import shutil
import glob
from PIL import Image


# Define a function to run a command using subprocess.run()
def run_command(command):
    print(command)
    try:
        result = subprocess.run(command)
    except:
        print("Error in command: ", command)

def get_file_list(path: str, search_string : str = ".ttr"):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.lower().endswith(search_string)
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


def average_corner_middle_colors(image_path: str) -> str:
    """
    Calculate the average color from the corners and middle edges of an image.

    Parameters:
    image_path (str): Path to the image file.

    Returns:
    str: HEX color representing the average of specified pixels.
    """
    with Image.open(image_path) as img:
        width, height = img.size

        # Define points to sample
        points = [
            # Top-left corner
            [(x, 0) for x in range(5)],
            # Top-right corner
            [(width - 1 - x, 0) for x in range(5)],
            # Bottom-right corner
            [(width - 1 - x, height - 1) for x in range(5)],
            # Bottom-left corner
            [(x, height - 1) for x in range(5)],
            # Middle top
            [(width // 2, y) for y in range(5)],
            # Middle bottom
            [(width // 2, height - 1 - y) for y in range(5)],
            # Right middle
            [(width - 1, height // 2 - 2 + y) for y in range(5)],
            # Left middle
            [(0, height // 2 - 2 + y) for y in range(5)]
        ]

        # Flatten the list of points and get unique values
        unique_points = list(set([point for sublist in points for point in sublist]))

        # Sum the color values
        total_color = [0, 0, 0]
        for point in unique_points:
            pixel = img.getpixel(point)
            print(pixel)
            total_color[0] += pixel[0]
            total_color[1] += pixel[1]
            total_color[2] += pixel[2]

        # Calculate average
        num_points = len(unique_points)
        avg_color = tuple(total // num_points for total in total_color)

        # Convert to HEX
        return '#{:02x}{:02x}{:02x}'.format(*avg_color)



if __name__ == "__main__":
    # Variations - Different Colors Used, Different Fonts or Different Test Strings
    # BRAND_NAMES = ["irs", "asb", "atb", "bankia", "inter", "banco_de_chile", "bankia", "bbt", "belize", "bet365", "caf", "ing", "inter", "irs"]

    # BRAND_NAMES = ["crate&barrel", "cetelem", "daum", "dkb", "equa_bank", "free", "giffgaff", "hff", "iinet", "infinisource", "belize_bank", "caf", "cetelem","crate&barrel", "daum", "dkb", "equa_bank", "free", "giffgaff", "hff", "iinet", "ing", "irs", "luno", "m&t", "magulu", "match", "mbna", "mobile", "naver", "neteller", "optus", "orange", "ourtime", "rakuten", "seniorpeoplemeet", "sfr", "sharp", "simpliee", "spectrum", "stripe", "sunrise", "talktalk", "taxact", "telstra", "timeweb", "typeform", "uber", "urssaf", "verizon", "visa", "webmail", "wells_fargo", "wp60", "yandex", "zoopla", ""infinisource"]
    #["belize", "caf", "cetelem","crate&barrel", "daum", "dkb", "equa_bank", "free", "giffgaff", "hff", "iinet", "ing", "irs", "luno", "m&t"]

    #BRAND_NAMES = ["magaldu", "match", "mbna", "mobile", "naver", "neteller", "optus", "orange", "ourtime", "rakuten", "seniorpeoplemeet", "sfr", "sharp", "simpliee", "spectrum", "stripe", "sunrise", "talktalk", "taxact", "telstra", "timeweb", "typeform", "uber", "urssaf", "verizon", "visa", "webmail", "wells_fargo", "wp60", "yandex", "zoopla"]
    
    #BRAND_NAMES = ["adp", "airdbnb", "bcp", "blizzard", "cox", "discover", "facebook", "frontier", "gmx", "itau", "knab", "luno", "meridian", "td", "tsb", "we", "ziggo"] 
    
    #BRAND_NAMES = ["simplii", "spectrum", "stripe", "sunrise", "talktalk", "taxact", "telstra", "timeweb", "typeform", "uber", "urssaf", "verizon", "visa", "webmail", "wells_fargo", "wp60", "yandex", "zoopla", "meridian", "td", "tsb", "we", "ziggo"]

    # BRAND_NAMES = ["infinisource", "facebook", "timeweb", "typeform", "uber", "verizon", "webmail", "wp60", "yandex"]

    BRAND_NAMES = ["caixa"]
    
    for BRAND_NAME in BRAND_NAMES:
        # FONT_DIR = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/google-open-source-fonts/all_fonts/"
        OUTPUT_DIR = '../../generated_fonts/new_brands/' + BRAND_NAME + "/"
        INPUT_FILE = '../../inputs/new_brands/' + BRAND_NAME + "/" + "input.txt"
        COLOR_INPUT_FILE = "../../inputs/new_brands/" + BRAND_NAME + "/color_schemes/colors1.json"

        OG_FONT_FOLDER =  f"/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/screenshots/new_fonts/final_fonts/{BRAND_NAME}"

        png_file_list = get_file_list(OG_FONT_FOLDER, ".png")

        colors_file = json.load(open(COLOR_INPUT_FILE))

        if "bg" not in colors_file:
            try:
                background_color = average_corner_middle_colors(png_file_list[0])
            except:
                background_color = "#FFFFFF"
        else:
            background_color = colors_file["bg"]

        # FONTS = ["spotify-font", "gotham-rounded", "montserrat", "arial", "helvetica", "helvetica-neue"]
        COLOR_VARS = [COLOR_INPUT_FILE]
        STROKE_WIDTH_VARS = ['0']
        STROKE_FILL_COLORS_VARS = ["#000000"]
        CHAR_SPACE_VARS = ['0']
        ALIGNMENT_VARS = ['0']

        MARGIN = 20
        c = 0

        GLOBAL_FONT_DIR = f"/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/font_generation/fonts"

  
        FONT_TYPE_PATHS = ["custom-fonts", "google-open-source-fonts"]
        
        for font_type_path in FONT_TYPE_PATHS:
            CURRENT_FONT_DIR = os.path.join(GLOBAL_FONT_DIR, font_type_path)
            FONT_FOLDERS = get_folder_list(CURRENT_FONT_DIR)

            make_directory_tree(OUTPUT_DIR + font_type_path + "/")

            commands = []

            for FONT_NO, FONT_DIR in enumerate(FONT_FOLDERS):
                fonts = get_file_list(FONT_DIR, ".ttf")

                final_fonts = get_ttf_files(FONT_DIR)
                # print("Before Moving = ",len(final_fonts))

                for font_path in fonts:
                    font_name = font_path.split("/")[-1]
                    check_path = FONT_DIR + "/" + font_name

                    if check_file_exists(check_path) == False:
                        copy_file(font_path, check_path)
                
                final_fonts = get_ttf_files(FONT_DIR)
                len_fonts = len(final_fonts)

                FONT_OUTPUT_DIR = OUTPUT_DIR + font_type_path + "/" + FONT_DIR.split("/")[-1] + "/"
                
                make_directory_tree(FONT_OUTPUT_DIR)

                
                for COLOR in COLOR_VARS:
                    for STROKE in STROKE_WIDTH_VARS:
                        for STROKE_FILL_COLOR in STROKE_FILL_COLORS_VARS:
                            for CHAR_SPACE in CHAR_SPACE_VARS:
                                for ALIGNMENT in ALIGNMENT_VARS:
                                    commands.append(['python3.7', 'run.py',
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
                                                    '--background', '5',
                                                    '--background_color', background_color,
                                                    "--alignment", str(ALIGNMENT),
                                                    "--character_spacing", str(CHAR_SPACE)
                                                    ])
                                    c += 1

                print("Number of Commands = ", len(commands))

                appendToCSV([FONT_DIR.split("/")[-1], len_fonts], OUTPUT_DIR + font_type_path + "/" + "check_fonts.csv", verbose = True)
        
                if (FONT_NO % 25 == 0) and (FONT_NO != 0):
                    # Create a multiprocessing pool with the number of processes you want to use
                    pool = multiprocessing.Pool(processes = 100)

                    # Run each command in a separate process using the pool.map() method
                    pool.map(run_command, commands)

                    # Close the pool to prevent any more tasks from being submitted to it
                    pool.close()

                    # Wait for all processes to finish
                    pool.join()

                    commands = []

                