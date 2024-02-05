import os
import argparse
from datasets import load_dataset
import pandas as pd
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data ingestion script')

    parser.add_argument(
        '--data_filename', 
        type=str, 
        default='data',
        help='Data file name'
    )

    return parser.parse_args()

def download_dataset(data_filename: str):
    if os.path.exists(f'./data/{data_filename}.csv'):
        print('Data file with given name already exists, skipping data downloading')
    else:
        load_dataset("sentiment140")['train'].to_csv(f"./data/{data_filename}.csv")

def clean_text(text):
    text = re.sub('@[^\s]+','user',text) #Remove usernames
    text = re.sub('http[^\s]+','link',text) #Remove links
    text = " ".join(text.split()) #Remove excess whitespaces
    
    return text

def process_data(data: pd.DataFrame):
    data = data.drop(['date', 'query', 'user'], axis = 1)

    data.sentiment = data.sentiment.map({
        0 : 0,
        4 : 1
        })
    
    #Remove usernames, links and excessive whitespaces from texts
    data['text'] = data['text'].apply(clean_text)

    return data

def main(data_filename: str):
    download_dataset(data_filename)
    process_data(pd.read_csv(f"./data/{data_filename}.csv")).to_csv(f"./data/{data_filename}_processed.csv")


if __name__ == '__main__':
    args = parse_arguments()
    main(args.data_filename)