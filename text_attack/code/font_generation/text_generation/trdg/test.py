import subprocess
import os
import webcolors
import multiprocessing

# Define a function to run a command using subprocess.run()
def run_command(command):
    print(command)
    result = subprocess.run(command)

def get_ttf_file_list(path: str):
    """Get a list of all .ttf files in a directory and its subdirectories"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(".ttf")
    ]

if __name__ == "__main__":
    FONT_DIR_ADDR = './fonts/custom/'
    OUTPUT_DIR = './output/test/'
    INPUT_FILE = '../input.txt'

    FONTS = ['amatic','capture_it','lato','pacifico','raleway','sansation','nunito','open_sans','roboto','quicksand','inconsolata']
    # COLOR_VARS = ['#127CD6']
    # STROKE_WIDTH_VARS = ['0', '1']
    # STROKE_FILL_COLORS_VARS = ['#0000FF','#00A2ED','#FFFFFF']
    # CHAR_SPACE_VARS = ['-1', '0', '1']
    # ALIGNMENT_VARS = ['0', '1']
    # DISTORTION_VARS = ['0','1']
    # DISTORTION_ORIENTATION_VARS = ['0','1']

    "/Users/niravdiwan/Desktop/text_gen/phish_visualization/text_generation/trdg/fonts/ar"
    MARGIN = 1

    c = 0

    commands = []
    COLOR = '#127CD6'

    for FONT in FONTS:
        
        FONT_DIR = FONT_DIR_ADDR + FONT + '/'
        FONT_OUTPUT_DIR = OUTPUT_DIR + '/' + FONT

        nf_ttf_files = len(get_ttf_file_list(FONT_DIR))

        # commands.append(['python3', 'run.py',
        #             '--input_file', INPUT_FILE,
        #             '--count', str(nf_ttf_files),
        #             '--text_color',  COLOR_VARS[0],
        #             '--font_dir', FONT_DIR,
        #             '--output_dir', FONT_OUTPUT_DIR,
        #             '--margin', str(MARGIN),
        #             '--format', str(64),
        #             '--name_format', str(3),
        #             ])

        commands.append(['python3', 'run.py',
                            '--input_file', INPUT_FILE,
                            '--count', str(nf_ttf_files),
                            '--output_dir', FONT_OUTPUT_DIR,
                            '-om', '256',
                            '-obb', '1',
                        ])

    # Create a multiprocessing pool with the number of processes you want to use
    pool = multiprocessing.Pool(processes = 10)

    # Run each command in a separate process using the pool.map() method
    pool.map(run_command, commands)

    # Close the pool to prevent any more tasks from being submitted to it
    pool.close()

    # Wait for all processes to finish
    pool.join()


