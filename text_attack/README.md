# Adversarial-Text-Font-Generation

## Table of Contents
1. [Overview](#overview)
2. [Downloads](#downloads)
3. [Virtual Environments](#virtual-environments)
4. [Environment & Setup Activation](#environment--setup-activation)
5. [Running End to End Evaluations](#running-end-to-end-evaluations)
6. [Input Directory Structure](#input-directory-structure)
7. [File Descriptions](#file-descriptions)

## Overview
There are two main components in this project:
1. Font Generation
2. Font Selection

## Downloads
Download Phishintention from the following link and place it in `code/font_selection/phishintention`:
[Phishintention Download](https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing)

Download the fonts from the following link and place them in `data/`:
[Fonts Download](https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing)

## Virtual Environments
Our virtual environment files are located as follows:

1. Font Generation Environment - `Adversarial-Text-Font-Generation/font_gen_environment.yml`
2. Font Selection Environment - `Adversarial-Text-Font-Generation/phishintention_environment.yml`

Our program uses two virtual environments. The first virtual environment is used for font generation and the second virtual environment is used for font selection. This is because font generation is inspired by the TRDG library which requires Python 3.9, whereas font selection uses Phishintention which requires Python 3.7.4 and some very specific dependencies such as Detecton2 (0.6).

## Environment & Setup Activation
```bash
conda env create --name env_font_gen --file=font_gen_environment.yml
conda env create --name env_font_selec --file=phishintention_environment.yml
```

Set up the font selection environment:
```bash
conda activate env_font_selec
cd code/font_selection/phishintention
python setup.py install
```

The installation may take a while. This might give an error for sklearn package. 

#### Font Selection Environment Setup
```
conda activate env_font_gen
``` 

### Run End to End Evals for all 15 main brands on End to End
```
cd code/font_selection
bash all_brand_evals.sh
```

### Input

- input
  - [BRAND_NAME]
    - font_gen
      - colors.json
      - logo_text.txt
    - info.txt
    - logo_position.pt
    - orig_logo.png
    - screenshot.png

Each of these files are described in the [File Descriptions](#file-descriptions) section. They are necessary for the font generation and selection process.

## File Descriptions

logo_text.txt - contains the text of the logo

colors.json - contains the colors of the logo for each index in HEX format.

For instance, Amazon logo has the text "amazon" and each character is colored as black. Therefore, the colors.json file for Amazon would look like this:
```
{
    "0" : "#000000",
    "1" : "#000000",
    "2" : "#000000",
    "3" : "#000000",
    "4" : "#000000",
    "5" : "#000000"
}
``` 


info.txt - contains the brand name, and this file is used by Phishintention. To create it for a new brand, just copy the info.txt file from another brand and change the brand name.

logo_position.pt - contains the position of the logo in the screenshot. This file is created by running the get_logo_position.py script in the code/font_selection folder.

orig_logo.png - contains the original logo of the brand

screenshot.png - contains the screenshot of the website


<!-- ### Cropping Ground Truth Fonts from the Target Screenshot

1. Store the target screenshot in screenhots/original/{type_of_logo}/{brand}/screenshots/
2. Activate the phishintention virtual environment
3. Run the get_cropped_font.py in phish_intension/Phishintention

### Generating Candidate Fonts

1. Activate the fontgen virtual environment
2. Create 

### Posit Candidate Fonts to the Target Screenshot
1. 

### Test Phishintention on Candidate Fonts -->