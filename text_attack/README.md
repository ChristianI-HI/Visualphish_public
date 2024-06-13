# Adversarial-Text-Font-Generation

There are two main components in this project:
1. Font Generation
2. Font Selection

The Font Generation uses


## Downloads
Download Phishintention from the following link and place it in code/font_selection/phishintention
https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing

Download the fonts from the following link and place it in data/
https://drive.google.com/drive/folders/1yYga_zrRyGtcJpJiiH-iWVuGTPU90lyN?usp=sharing


## Virtual Environments
Our virtual environment files are located 

1. Font Generation Environment - ```Adversarial-Text-Font-Generation/font_gen_environment.yml```
2. Font Selection Environment - ```Adversarial-Text-Font-Generation/phishintention_environment.yml```. 

Unusally, our program uses two virtual environments. The first virtual environment is used for the font generation and the second virtual environment is used for the font selection. This is because the font generation is inspired from the trdg library which requires python 3.9
whereas the font selection uses phishintention which requires python 3.7.4 and some very specific dependencices - detecton2 (0.6).

We encourage the reviewers to start the process eraly, Although we have thoroughly tested the program and created the respective environment files with, there might be some issues with the installation of the dependencies. If you encounter any issues, please let us know.

### Environment & Setup Activation
```
conda env create --name env_font_gen --file=font_gen_environment.yml
conda env create --name env_font_selec --file=phishintention_environment.yml
```

#### Font Selection Environment Setup
```
conda activate env_font_gen
``` 

### Run Evals on End to End Experiments
```
cd code/font_selection
bash all_brand_evals.sh
```

### Font Generation

### Font Selection


### Cropping Ground Truth Fonts from the Target Screenshot

1. Store the target screenshot in screenhots/original/{type_of_logo}/{brand}/screenshots/
2. Activate the phishintention virtual environment
3. Run the get_cropped_font.py in phish_intension/Phishintention

### Generating Candidate Fonts

1. Activate the fontgen virtual environment
2. Create 

### Posit Candidate Fonts to the Target Screenshot
1. 

### Test Phishintention on Candidate Fonts