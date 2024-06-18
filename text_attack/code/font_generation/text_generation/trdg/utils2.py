import os
import shutil


def get_all_ttf_files(folder):
    """Get a list of all .ttf filepaths in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(folder)
        for file in files
        if file.endswith(".ttf")
    ]

def copy_files(filelist, folder2):
    """Copy a list of files to a folder"""
    for file in filelist:
        shutil.copy(file, folder2)

if __name__ == "__main__":
    PATH = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/google-open-source-fonts/"
    files = get_all_ttf_files(PATH)
    print(len(files))
    OUT_PATH = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/google-open-source-fonts/all_fonts/"
    copy_files(files, OUT_PATH)

    