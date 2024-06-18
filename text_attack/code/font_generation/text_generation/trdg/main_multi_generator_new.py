import subprocess
import os
import webcolors
import multiprocessing

# Define a function to run a command using subprocess.run()
def run_command(command):
    print(command)
    try:
        result = subprocess.run(command)
    except:
        print("Error in command: ", command)

def get_ttf_file_list(path: str):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(".ttf") or file.endswith(".TTF")
    ]

def get_folder_list(directory):
    """Get a list of all folders in a directory"""
    return [
        os.path.join(directory, folder)
        for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]


if __name__ == "__main__":

    # Variations - Different Colors Used, Different Fonts or Different Test

    BRAND_NAME = "yahoo"
    FONT_DIR = '../../fonts/latin-font-family/'
    FONT_DIR = "/Users/niravdiwan/Desktop/text_gen/phish_visualization/fonts/google-open-source-fonts/all_fonts/"
    OUTPUT_DIR = '../../generated_fonts/' + BRAND_NAME + "/try/"
    INPUT_FILE = '../../inputs/' + BRAND_NAME + ".txt"

    # FONTS = ["spotify-font", "gotham-rounded", "montserrat", "arial", "helvetica", "helvetica-neue"]
    COLOR_VARS = ['#000000']
    STROKE_WIDTH_VARS = ['0']
    STROKE_FILL_COLORS_VARS = ["#000000"]
    CHAR_SPACE_VARS = ['0']
    ALIGNMENT_VARS = ['0']

    MARGIN = 20
    
    c = 0
    commands = []

    fonts = get_ttf_file_list(FONT_DIR)
    len_fonts = len(fonts)
    print(len_fonts)

    for COLOR in COLOR_VARS:
        for STROKE in STROKE_WIDTH_VARS:
            for STROKE_FILL_COLOR in STROKE_FILL_COLORS_VARS:
                for CHAR_SPACE in CHAR_SPACE_VARS:
                    for ALIGNMENT in ALIGNMENT_VARS:
                        commands.append(['python3', 'run.py',
                                        '--input_file', INPUT_FILE,
                                        '--text_color', COLOR,
                                        '--count', str(len_fonts), 
                                        '--font_dir', FONT_DIR,
                                        '--output_dir', OUTPUT_DIR,
                                        '--name_format', str(3),
                                        '--margin', str(MARGIN),
                                        '--stroke_width', str(STROKE),
                                        '--stroke_fill', str(STROKE_FILL_COLOR), 
                                        '--format', str(256),
                                        '--background', '1',
                                        "--alignment", str(ALIGNMENT),
                                        "--character_spacing", str(CHAR_SPACE)
                                        ])
                        c += 1

    # Create a multiprocessing pool with the number of processes you want to use
    pool = multiprocessing.Pool(processes = 10)

    # Run each command in a separate process using the pool.map() method
    pool.map(run_command, commands)

    # Close the pool to prevent any more tasks from being submitted to it
    pool.close()

    # Wait for all processes to finish
    pool.join()