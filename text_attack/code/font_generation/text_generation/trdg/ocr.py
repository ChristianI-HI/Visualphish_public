import pytesseract
from PIL import Image
import os
from pathlib import Path
import csv

def appendToCSV(row, filepath, verbose = True):
	"""
	Appends a csv 
	"""
	if verbose == True: print(row, 'appending into', filepath, '.........')
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	if verbose == True: print('Appended')

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

import os
import shutil


def copy_file(original_file_path, target_file_path):
    """
    Copies a file from original_file_path to target_file_path
    """
    try:
        shutil.copy(original_file_path, target_file_path)
        print('Copied', original_file_path, 'to', target_file_path)
    except:
        print('Error copying', original_file_path, 'to', target_file_path)

def make_directory_tree(pathname):
	"""
	Creats  hierarchical paths
	"""
	path = Path(pathname)
	path.mkdir(parents = True, exist_ok = True)


fonts = ['lato', 'inconsolata','nunito','open_sans','roboto','quicksand']

for font_name in fonts:
    folderpath = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/output/" + font_name + "/"
    files = get_file_list(folderpath, sort = True, verbose = False)

    no_text = []
    non_logo = []
    output_file = '/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/output/ocr_fail_output.csv'
    no_text_file = '/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/output/no_text_output.csv'

    c = 0

    ignore_list = ['_azure_','_cyan_','sfred','sflime']

    for file in files:
        check = False
        
        for ignore_item in ignore_list:
            if ignore_item in file:
                check = True
                break

        if check == True:
            continue
        
        
        # image = Image.open('/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/output/lato/Outlook_blue_sw0_sfturquoise_sk0_bl1_d1_do1_cs0.jpg')
        image = Image.open(folderpath + file)
        text = pytesseract.image_to_string(image)
        
        target_file_folder = '/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/output/ocr_fail/' + font_name + '/'

        make_directory_tree(target_file_folder)

        if len(text.strip().lower()) == 0:
            #print('No text detected')
            no_text.append(file)
            appendToCSV([font_name, file], no_text_file, verbose = False)
        elif text.strip().lower() != 'Outlook'.lower():
            #print('Outlook logo detected')
            non_logo.append(file)
            appendToCSV([font_name, file, text.strip().lower()], output_file, verbose = False)
            copy_file(folderpath + file, target_file_folder + file)
        
        if c % 1000 == 0:
            print('Completed', c, 'files', file)

        c += 1
        




# text = pytesseract.image_to_string(image)
# print(text)