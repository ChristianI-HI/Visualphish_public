#!/bin/bash

# Set CUDA device order and visibility
export CUDA_DEVICE_ORDER="PCI_BUS_ID"
export CUDA_VISIBLE_DEVICES='7'

# Define constants for the other parameters
THRESHOLD=0.87
K=200
DEVICE="cuda"
FONT_GEN_ENVIRONMENT="env_font_gen"
PHISHINTENTION_ENV="env_font_selec"

# List of brands from the image
BRANDS=("instagram" "amazon" "boa" "chase" "comcast" "google" "docusign" "dropbox" "ebay" "linkedin" "netflix" "outlook" "paypal" "spotify" "yahoo")

Loop through each brand and run the scripts
for BRAND_NAME in "${BRANDS[@]}"; do
    echo "Processing $BRAND_NAME"
    ./main_brand_evals.sh $BRAND_NAME $THRESHOLD $K $DEVICE $FONT_GEN_ENVIRONMENT $PHISHINTENTION_ENV
    echo "Completed processing for $BRAND_NAME"
done

echo "All brands processed."
conda activate $PHISHINTENTION_ENV
cd scripts
for BRAND_NAME in "${BRANDS[@]}"; do
    echo "Getting Results for $BRAND_NAME"
    python3 collate_results.py --brand_name $BRAND_NAME --k $K
    echo "Completed processing for $BRAND_NAME"
done
cd ..
conda deactivate