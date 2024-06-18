# Adversarial-Text-Font-Generation
This folder contains the code for the text attack for the paper.

## Table of Contents
1. [Overview](#overview)
2. [Setup](#setup)
   - [Downloads](#downloads)
   - [Virtual Environments](#virtual-environments)
   - [Environment & Setup Activation](#environment--setup-activation)
3. [Running Evaluations](#running-evaluations)
   - [Reproduce Results for a Brand](#reproduce-results-for-a-brand)
   - [Reproduce Results for all 15 Brands](#reproduce-results-for-all-15-brands)
4. [Input Directory Structure](#input-directory-structure)
5. [File Descriptions](#file-descriptions)
6. [Add a New Brand to Attack](#add-a-new-brand-to-attack)
7. [Contributing](#contributing)

## Overview
There are two main components in this project:

1. Font Generation - Using our database on fonts, we generate a set of candidate fonts that are similar to the original logo. We use the TRDG library to generate these fonts.

2. Font Selection - We select the top K fonts that are most similar to the original logo using the OCR similarity score. We paste the logos back on the screenshot and pass them through Phishintention to evaluate the effectiveness of the attack.

## Setup

### Downloads
Download Phishintention code from the following link and place it in `code/font_selection/phishintention`:
[Phishintention Download](https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing)

This code is an earlier version of Phishintention that we modified to work with our code. 

Download the fonts from the following link and place them in `data/`:
[Fonts Download](https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing)

### Virtual Environments
Our virtual environment files are located as follows:

1. Font Generation Environment - `Adversarial-Text-Font-Generation/font_gen_environment.yml`
2. Font Selection Environment - `Adversarial-Text-Font-Generation/phishintention_environment.yml`

Our program uses two virtual environments. The first virtual environment is used for font generation and the second virtual environment is used for font selection. This is because font generation is inspired by the TRDG library which requires Python 3.9, whereas font selection uses Phishintention which requires Python 3.7.4 and some very specific dependencies such as Detecton2 (0.6).

The trdg library can be found here:
https://github.com/Belval/TextRecognitionDataGenerator/tree/master

The Original Phishintention library can be found here:
https://github.com/lindsey98/PhishIntention


### Environment & Setup Activation
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

The installation may take a while. After setting up the build for the majority of the packages, it might give an error for sklearn package. However, the package is not needed for the code to run. 

### Activating & Deactivating the Environments

The environments can be activated and deactivated using the following commands:


```
conda activate env_font_gen
conda deactivate
``` 

```
conda activate env_font_selec
conda deactivate
``` 

## Reproduce Results for a Brand

The file to run generation and evaluation for a specific brand is main_brand_evals.sh. 
You can run the script by running the following commands:

```
cd code/font_selection
bash main_brand_evals.sh
```

The script automatically activates and deactivates the environments. Make sure that the brand name is set to the brand you want to run the evaluation for.

#### Parameters

The main parameters for the font generation are:
- `BRAND_NAME` - The brand name for which the font selection is to be done. The brand name should be one of the 15 main brands mentioned in input folder.

- `THRESHOLD` - The threshold for the OCR and Phishintention similarity score. The default value is 0.87.

- `K` - The number of top fonts to be selected for the brand. The default value is 200.

- `DEVICE` - The device to run Phishintention on. The default value is 'cuda'. To set the GPU device number, manually set the device number in the script on third line as 
export CUDA_VISIBLE_DEVICES= 'device_number'.

- `FONT_GEN_ENVIRONMENT` - The name of the font generation environment. The default value is 'env_font_gen'.

- `FONT_SELEC_ENVIRONMENT` - The name of the font selection environment. The default value is 'env_font_selec'.

### Reproduce Results for all 15 Brand

The file to run generation and evaluation for all brands is all_brand_evals.sh.
You can run the script by running the following commands:

```
cd code/font_selection
bash all_brand_evals.sh
```

It just sequentially runs the main_brand_evals.sh script for all the listed 15 brands.

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


### Output
- output
  - [BRAND_NAME]
    - logos
      - custom-fonts
        - [FONT_NAME]
          - [FONT_ID]\_[FONT_NAME].png
      - google-open-source-fonts
        - [FONT_NAME]
          - [FONT_ID]\_[FONT_NAME].png
    - screenshots
      - top_[K]
        - all
           - [FONT_ID]\_[FONT_NAME]\_[OCR_SIM_SCORE].png
        - failure
           - [FONT_ID]\_[FONT_NAME]\_[OCR_SIM_SCORE]\_[END2END_PHISHINTENTION_SCORE].png
        - success
          - [FONT_ID]\_[FONT_NAME]\_[OCR_SIM_SCORE]\_[END2END_PHISHINTENTION_SCORE].png
    - top_K_logos
      - [FONT_ID]\_[FONT_NAME]\_[OCR_SIM_SCORE].png


FONT_NAME, BRAND_NAME and K are self explanatory.

FONT_ID - This is the font_id assigned to the font. Checkout the 
OCR_SIM_SCORE - The OCR Similarity Score of the FONT.
END2END_PHISHINTENTION_SCORE - The End2End Final Phishintention score assigned to the font.

## Input File Descriptions

1. `screenshot.png` - contains the screenshot we aim to attack. In all our experiments, we used the  Phishintention. To create it for a new brand, 

2. `orig_logo.png` - This is the cropped logo from the screenshot. 

3. `logo_position.pt` - contains the position of the logo in the screenshot. 

4. `font_gen/logo_text.txt` - contains the text of the logo. Retains the case of the text. For instance, the logo text for Amazon would be "amazon".

5. `font_gen/colors.json` - contains the colors of the logo for each index in HEX format.For instance, Amazon logo has the text "amazon" and each character is colored as black. 
Therefore, the colors.json file for Amazon would look like this:

```
{
    "0" : "#000000", #a
    "1" : "#000000", #m
    "2" : "#000000", #a
    "3" : "#000000", #z
    "4" : "#000000", #o
    "5" : "#000000"  #n
}
``` 

You can also specify the background color of the logo by adding a key "background" in the colors.json file. For instance, the colors.json file for Amazon with a white background would look like this:

```
{
    "0" : "#000000", #a
    "1" : "#000000", #m
    "2" : "#000000", #a
    "3" : "#000000", #z
    "4" : "#000000", #o
    "5" : "#000000", #n
    "bg_color" : "#FFFFFF"
}
```

If the background color is not specified, we calculate an approximate background color by taking the average of the corners of the `orig_logo.png` image.

6. `info.txt` - contains the brand name, and this file is used by Phishintention. To create it for a new brand, just copy the info.txt file from another brand and change the brand name.


## Add a new brand to attack

To add a new brand to attack, you need to create a new folder in the input directory with the brand name. The folder should contain all the files mentioned in the [Input File Descriptions](#input-file-descriptions) section.


## Time Taken
For the end2end evaluation of one font it takes about 20 min. Therefore, for K fonts, it takes about 20 * K minutes. For the 15 brands, it takes about 5 hours.


## 👪 Contributing
For the text attack, pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. For any detailed clarifications/issues, please email to ndiwan2[at]illinois[dot]edu[dot].


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