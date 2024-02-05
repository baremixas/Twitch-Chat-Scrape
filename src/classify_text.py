import argparse
import pandas as pd
import tensorflow as tf
import numpy as np
from model_training import tokenize_text


def parse_arguments():
    parser = argparse.ArgumentParser(description='Main script')

    parser.add_argument(
        '--model_name', 
        type=str, 
        default='model',
        help='Model name'
    ),
    parser.add_argument(
        '--texts_filename', 
        type=str, 
        default='texts', 
        help='Texts file name'
    ),
    parser.add_argument(
        '--results_filename', 
        type=str, 
        default='results', 
        help='Results file name'
    )

    return parser.parse_args()

def get_data(texts_filename: str):
    try:
        data = pd.read_csv(f'./data/{texts_filename}.csv')
    except FileNotFoundError:
        print ("Wrong file or file path")
        data = pd.DataFrame({'user': [], 'text': []})

    return data

def detect_sentiment(data: pd.DataFrame, model_name: str, results_filename: str):
    model = tf.keras.models.load_model(f'./models/{model_name}.h5')

    padded_texts = tokenize_text(data['text'])

    predictions = model.predict(padded_texts)

    data['predictions'] = predictions

    data['sentiment'] = data['predictions'].apply(lambda x: 'Negative' if x < 0.5 else 'Positive')

    data.to_csv(f"./results/{results_filename}.csv")
    

def main(model_name: str, texts_filename: str, results_filename: str):
    data = get_data(texts_filename)
    detect_sentiment(data, model_name, results_filename)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.model_name, args.texts_filename, args.results_filename)