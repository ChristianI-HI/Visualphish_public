import otf2ttf
import os
from pathlib import Path
import subprocess

def get_otf_file_list(path: str):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".otf"):
                x = os.path.join(root, file)
                x = convert_to_linux_path(x)
                x = x.replace("\\ ", " ")
                # print(x)
                # print("DOES PATH EXIST?" + str(os.path.exists(x)))
                subprocess.call(['otf2ttf', x])


if __name__ == "__main__":
    DIR_PATH = "/Users/niravdiwan/Desktop/text_gen/fonts"
    otfFiles = get_otf_file_list(DIR_PATH)

    # for otfFilePath in otfFiles:
    #     print(otfFilePath)
    #     otfFilePath1 = Path(otfFilePath)
    #     # otfFilePath1 = os.path.normpath(otfFilePath)
    #     print(str(otfFilePath1))
    #     os.system("otf2ttf " +  str(otfFilePath1))



    # for file in os.listdir(DIR_PATH):
    #     print(file)
    #     if file.endswith(".otf"):
            


