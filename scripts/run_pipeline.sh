#!/bin/bash

# You can run this script from command line using:
# ./scripts/run_pipeline.sh

# Get command line arguments
file_name="$1"
stream_name="$2"
delay="$3"

echo "Starting data ingestion..."
python src/data_ingestion.py --file_name="$file_name"

#echo "Starting model training..."
#python src/model_training.py --file_name="$file_name"+"_processed"

echo "Starting scraping text..."
python src/scrape_text.py --stream_name="$stream_name" --delay="$delay"

echo "Pipeline completed."
