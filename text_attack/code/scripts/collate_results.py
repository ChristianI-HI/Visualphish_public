import sys
sys.path.append('../..')
from paths import PROJECT_PATH
from read_write_fns import *
import argparse

def get_params():
    """Take in the file from the command line"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--brand_name', type=str, default= "instagram", help='Testing on which dataset')
    parser.add_argument('--k', type=int, default= 200, help='Number of Top k logos to be selected')

    args = parser.parse_args()
    return args.brand_name, args.k

if __name__ == "__main__":

    BRAND_NAME, TOP_K = get_params()
    results = loadJsonFile(f"{PROJECT_PATH}/data/output/{BRAND_NAME}/screenshots/top_{TOP_K}/results.json")

    print(f"----------- {BRAND_NAME} Results -----------")
    print("Success/Total")
    print(f"{results["success"]}/{results["total"]}")
    