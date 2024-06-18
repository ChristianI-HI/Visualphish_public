import sys
sys.path.append('../..')
from paths import PROJECT_PATH
from read_write_fns import *
import shutil

print("Hello World!")
files = get_files_with_string_in_name_deep(f"{PROJECT_PATH}/data/fonts", ".ttf")

id_to_info = {}
name_to_info = {}

filesets = set()

print(len(files))

file_id = 0

for file_no, file in enumerate(files):
    filename = file.split('/')[-1]

    filepath = file.replace("/home/ndiwan2/projects/adversarial_logo/Adversarial-Text-Font-Generation/", "")

    if filename not in filesets:
        filesets.add(filename)

        id_to_info[file_id] = {
                                "name" : filename,
                                "path" : filepath
                              }
        
        name_to_info[filename] = {
                                "id" : file_id,
                                "path" : filepath
        }
        file_id += 1


dumpJsonFile(id_to_info, f"{PROJECT_PATH}/data/fonts/font_id_to_info.json")
dumpJsonFile(name_to_info, f"{PROJECT_PATH}/data/fonts/font_name_to_info.json")

# for key in id_to_info.keys():
#     localfilepath = "/".join(id_to_info[key]["path"].split("/")[3:])

#     source_dst = f"{PROJECT_PATH}{id_to_info[key]['path']}"
#     target_dst = f"{PROJECT_PATH}data/final_fonts/{localfilepath}"

#     print(source_dst)
#     print(target_dst)
    
#     # Copy file from source to target
#     target_folder_path = "/".join(target_dst.split("/")[:-1])
#     if not os.path.exists(target_folder_path):
#         os.makedirs(target_folder_path)

#     shutil.copy(source_dst, target_dst)
