import json
import pickle
import csv
import sys
import datetime
import numpy as np
import random
import os
import pathlib
from pathlib import Path
import shutil

import os

def create_folders_path(path_name):
    path = pathlib.Path(path_name)
    path.parent.mkdir(parents = True,exist_ok = True)
    
def make_directory_tree(pathname):
	"""
	Creats  hierarchical paths
	"""
	path = Path(pathname)
	path.mkdir(parents = True, exist_ok = True)

def loadPickleFile(filepath):
	#print("Loading the pickle file from",filepath,"...........")
	pickle_in = open(filepath,"rb")
	example_dict = pickle.load(pickle_in)
	#print("Loaded the pickle File")
	return example_dict

def openCSVfile(filepath, delimiter = ","):
    """
    Returns the lists for csv file 
    """
    with open(filepath,"r") as csvfile:
        rows =  csv.reader(csvfile,delimiter = delimiter)
        return list(rows)

def appendToCSV(row, filepath, verbose = True):
	"""
	Appends a csv 
	"""
	if verbose == True: print(row, 'appending into', filepath, '.........')
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	if verbose == True: print('Appended')

def dumpCSVfile(rows,filepath,verbose = True):
    """
    Dumps the csv file
    """
    if verbose == True: print('Dumping to', filepath, '.........')
    with open(filepath,"w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    if verbose == True: print('Dumped')
     

def dumpPickleFile(data,filepath):
	pickle_out = open(filepath,"wb")
	pickle.dump(data, pickle_out)
	pickle_out.close() 

def dumpJsonFile(dictionary,filepath):
	with open(filepath,"w+") as jsonFile:
		json.dump(dictionary,jsonFile,indent=4,sort_keys =True)

def loadJsonFile(filepath, verbose = True):
    if verbose:
        print(f"Loading from {filepath}...............")

    dictionary = {}
        
    with open(filepath, "rb") as jsonFile:
        dictionary = json.load(jsonFile)
    return dictionary

# Convert timestamp
def convert_timestamp(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    date_split = date.split("-");month = int(date_split[1]);year = int(date_split[0])
    return month,year,date

# def read_json_objects(filepath):
#     objects = [] 
#     with jsonlines.open(filepath) as reader:
#         for obj in reader:
#             created_timestamp = obj['created_utc']#;updated_timestamp = obj['updated_utc']
#             month,year,date = convert_timestamp(created_timestamp)
#             objects.append([obj,month,year,date])
#     return objects

def create_txt_file(filepath):
    """Create a txt file"""
    with open(filepath,"w") as txtFile:
        txtFile.write("")      

def get_arguments():
    n = len(sys.argv) 
    if n != 4:
        print('Incomplete not executing')
        sys.exit(0)
    print("Total arguments passed:", n) 
    print("\nName of Python script:", sys.argv[0]) 
    print("\nArguments passed:", end = " ") 
    
    model_name = sys.argv[1]
    class_name = sys.argv[2]
    json_filename = sys.argv[3]
    save_filename = sys.argv[4]
    
    return model_name, json_filename, save_filename

def get_txt_files(folder_path):
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def get_file_list(folderpath,sort = True,verbose = True):
	"""
	Returns a list of files inside a directory
	"""
	file_list = []
	
	for root,d_names,f_names in os.walk(folderpath):
		for fname in f_names:
			file_list.append(fname)
	# Sorting the list
	if sort == True:
		file_list.sort()

	print('File list is .....')
	if verbose == True:
		for file in file_list:
			print(file)

	return file_list

def load_file(filepath):
    """Load file as an array of strings split by newline"""
    with open(filepath, 'r') as f:
        file = f.read().splitlines()
    return file

def append_to_file(arr, filepath):
    """Add the elements of the array to the file separated by newline"""
    with open(filepath, 'a') as f:
        for line in arr:
            f.write(line)
            f.write("\n")
    return True

def get_files_with_string_in_name(directory, string):
    files = []
    for file in os.listdir(directory):
        if string in file:
            files.append(directory + file)
    return files

def get_files_with_string_in_name_deep(root, string):
    matching_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if string in name:
                matching_files.append(os.path.join(path, name))
    return matching_files


def check_file_exists(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False

def list_folders(directory):
    """
    List all folder names in the specified directory.

    Args:
    directory (str): The path to the directory.

    Returns:
    list: A list of folder names in the specified directory.
    """
    return [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]


def edit_and_save_brand(file_path, new_brand, save_file_path):
    try:
        # Read the content from the file
        with open(file_path, 'r') as file:
            data = file.read()
            dict_data = eval(data)  # Converts string to dictionary

        # Modify the brand
        dict_data['brand'] = new_brand

        # Write the modified dictionary back to the file
        with open(save_file_path, 'w') as file:
            file.write(str(dict_data))
        return "Brand updated successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_folder_list(directory):
    """Get a list of all folders in a directory"""
    return [
        os.path.join(directory, folder)
        for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]

# brand_names = list_folders("/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/screenshots/extended/original/new_brands/")

# orig_logo_folder_path = "/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/screenshots/extended"

# for brand_name in brand_names:
#     # Get the folder in
#     edit_and_save_brand(f"{orig_logo_folder_path}/original/adidas/info.txt", f"{brand_name}", f"{orig_logo_folder_path}/original/new_brands/{brand_name}/info.txt")

# folder_path = "/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/screenshots/new_fonts/final_fonts/"

# brand_names = list_folders(folder_path)

# values = "/data/phish_sample_30k"


# for brand_name in brand_names:
#     brand_name
     


# brand_names = list_folders("/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/top_200_success_fonts_phishpedia/transfer_fonts_all/")


# BRAND_NAME = "amazon"
# filepaths = get_files_with_string_in_name_deep(f"/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/top_200_success_fonts_phishpedia/amazon/", ".png")
# fileratings = []
# for filepath in filepaths:
#     # print(filepath)
#     rating = float(filepath.split("/")[-1][:-4].split("_")[-1])
#     fileratings.append((filepath, rating))

# fileratings.sort(key=lambda x: x[1])
# top_100_ratings = fileratings[:100]
# top_100_paths = [x[0] for x in top_100_ratings]


# print(fileratings[:5])
# print(fileratings[-5:])

# print(top_100_paths[:5])

# Copy the filepats to the new location
# print(len(top_100_paths))

# for path in top_100_paths:
#     filename = path.split("/")[-1]
#     destination_folder = f"/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/top_200_success_fonts_phishpedia/transfer_font_bottom_100/{BRAND_NAME}/"

#     # Create the folder if it does not exist
#     make_directory_tree(destination_folder)

#     # Copy the file using shutil
#     shutil.copy(path, f"{destination_folder}/{filename}")

# fontpaths = get_files_with_string_in_name_deep("/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/data/output/instagram/logos", ".jpg")

# fontids = loadJsonFile("/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/data/fonts/font_id_to_info.json")

# all_fontids = [int(i) for i in fontids.keys()]
# making_font_ids = []

# for fontpath in fontpaths:
#     font_id = int(fontpath.split("/")[-1].split("_")[0])
#     making_font_ids.append(font_id)

# all_fontids = set(all_fontids)
# making_font_ids = set(making_font_ids)

# missing_font_ids = all_fontids - making_font_ids


# for missing_font_id in missing_font_ids:
#     print(f"Missing font id: {missing_font_id}")
#     print(fontids[str(missing_font_id)]["name"])
#     print(fontids[str(missing_font_id)]["path"])



