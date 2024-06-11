import subprocess
import os

import csv
from pathlib import Path
import sys
import json
import shutil
import numpy as np
import glob
from PIL import Image

sys.path.append('../..')

# Define a function to run a command using subprocess.run()
def run_command(command):
    print(command)
    try:
        _ = subprocess.run(command)
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


def get_bg_color(colors_file_path, image_path):
    """
    """
    colors_file = json.load(open(colors_file_path))
    
    # Assign an initial background color
    background_color = "#FFFFFF"

    if "bg" in colors_file:
        # If the background color is provided in the colors file, use that
        background_color = colors_file["bg"]
    else:
        print(image_path)
        background_color = average_corner_middle_colors(image_path)
        print("Error in calculating background color. Using default color (#FFFFFF) instead.")

    return background_color


def resize_image(im1, im2):
    """
    Resizes the image
    """
    width1, height1 = im1.size
    # im2.thumbnail((width1, height1), Image.ANTIALIAS)
    im2.thumbnail((width1, height1), Image.Resampling.LANCZOS)
    return im2

def resize_image_from_path(image1_path, image2_path, save_img_path = None):
    """
    Resizes the image
    """
    im1, im2 = Image.open(image1_path), Image.open(image2_path)
    im2 = resize_image(im1, im2)
    if save_img_path:
        im2.save(save_img_path)
    return im2

def resize_to_retain_ratio(source_image_path, target_image_path, min_ratio = 1.0, fix_height = False):
    im1 = Image.open(source_image_path)
    
    if fix_height == False:
        target_image_width, _  = im1.size
    else:
        _, target_image_height  = im1.size

    # Resizing the target image
    im2 = Image.open(target_image_path)
    w, h = im2.size

    # Calculating the target image width
    ratio = h / float(w)

    if fix_height == False:
        target_image_height = int(np.floor(ratio * target_image_width))
    else:
        min_ratio = max(ratio, min_ratio)
        target_image_width = 1/ratio * target_image_height

    # Resizing the target image
    target_size = [int(target_image_width), int(target_image_height)]
    im2 = im2.resize(target_size)
    return im2

if __name__ == "__main__":
    pass