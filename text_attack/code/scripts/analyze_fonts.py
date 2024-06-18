
import sys
sys.path.append('../..')
from paths import PROJECT_PATH
from read_write_fns import *

files = get_files_with_string_in_name_deep(f"{PROJECT_PATH}/data/output/instagram/logos/", ".jpg")
print(len(files))