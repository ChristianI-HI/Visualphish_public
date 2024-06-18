#!/bin/bash

# Set CUDA device order and visibility
export CUDA_DEVICE_ORDER="PCI_BUS_ID"
export CUDA_VISIBLE_DEVICES='7'

source $HOME/miniconda3/etc/profile.d/conda.sh

# Set default values and use provided arguments if available
BRAND_NAME=${1:-"instagram"}
THRESHOLD=${2:-0.87}
K=${3:-200}
DEVICE=${4:-"cuda"}
FONT_GEN_ENVIRONMENT=${5:-"env_font_gen"}
PHISHINTENTION_ENV=${6:-"env_font_selec"}

Activate Font Generation environment and run the script
echo "Activating Font Generation environment..."
conda activate $FONT_GEN_ENVIRONMENT
echo "Running main.py for brand: $BRAND_NAME"
cd font_generation
python3 main.py --brand_name $BRAND_NAME
cd ..
echo "Deactivating Font Generation environment..."
conda deactivate

# Activate Phishing Intention environment and run the scripts
echo "Activating Phishing Intention environment..."
conda activate $PHISHINTENTION_ENV

cd font_selection
echo "Running ocr_eval.py for brand: $BRAND_NAME with threshold: $THRESHOLD and k: $K on device: $DEVICE"
python3 ocr_level_main.py --brand_name $BRAND_NAME --threshold $THRESHOLD --k $K --device $DEVICE
echo "Running screenshot.py for brand: $BRAND_NAME and k: $K"
python3 screenshot.py --brand_name $BRAND_NAME --k $K
echo "Running end2end_eval.py for brand: $BRAND_NAME with threshold: $THRESHOLD and k: $K on device: $DEVICE"
python3 end2end_eval.py --brand_name $BRAND_NAME --k $K --device $DEVICE
cd ..
echo "Deactivating Phishing Intention environment..."

cd scripts
echo "Getting Results for $BRAND_NAME"
python3 collate_results.py --brand_name $BRAND_NAME --k $K
echo "Completed processing for $BRAND_NAME"
cd ..

conda deactivate