
import os

def get_ttf_file_list(path: str) -> List[str]:
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(".ttf")
    ]

if __name__ == "__main__":
    print(get_ttf_file_list("/usr/share/fonts/truetype"))
