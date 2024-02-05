#!/bin/bash

# You can run this script from command line using:
# sh scripts/run_pipeline.sh "my_data" "my_model" "xqc" 2 0 "my_texts" "my_results"

# Insert headless bool value as: 0 for False or 1 for True

# Get command line arguments
data_filename="$1"
model_name="$2"
stream_name="$3"
delay="$4"
headless="$5"
texts_filename="$6"
results_filename="$7"

echo "Starting data ingestion..."
python src/data_ingestion.py --data_filename="$data_filename"

echo "Starting model training..."
python src/model_training.py --data_filename="$data_filename" --model_name="$model_name"

echo "Starting scraping text..."
python src/scrape_text.py --stream_name="$stream_name" --delay="$delay" --headless="$headless" --texts_filename="$texts_filename"

echo "Starting detecting sentiment from texts..."
python src/classify_text.py --model_name="$model_name" --texts_filename="$texts_filename" --results_filename="$results_filename"

echo "Pipeline completed."
