import tensorflow as tf
import pandas as pd
import argparse
import os
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class CONFIG:
    VOCAB_SIZE = 200000
    MAX_LENGTH = 50
    PADDING = 'post'
    EMBEDDING_DIM = 300

    TEST_SPLIT = .8
    VALIDATION_SPLIT = .2
    LEARNING_RATE = 0.01
    EPOCHS_NUMBER = 3
    BATCH_SIZE = 128


def parse_arguments():
    parser = argparse.ArgumentParser(description='Model training script')

    parser.add_argument(
        '--file_name', 
        type=str, 
        default='data',
        help='Data file name'
    ),
    parser.add_argument(
        '--model_name', 
        type=str, 
        default='model',
        help='Model file name'
    )

    return parser.parse_args()

def create_tokenizer(text_data: pd.Series):
    if os.path.exists('./data/tokenizer.pickle'):
        with open('./data/tokenizer.pickle', 'rb') as pickled_tokenizer:
            tokenizer = pickle.load(pickled_tokenizer)
    else:
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=CONFIG.VOCAB_SIZE)
        tokenizer.fit_on_texts(text_data)

        with open('./data/tokenizer.pickle', 'wb') as pickled_tokenizer:
            pickle.dump(tokenizer, pickled_tokenizer, protocol=pickle.HIGHEST_PROTOCOL)

    return tokenizer

def tokenize_text(text_data: pd.Series):
    tokenizer = create_tokenizer(text_data)

    sequences = tokenizer.texts_to_sequences(text_data)
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=CONFIG.MAX_LENGTH, value=CONFIG.VOCAB_SIZE-1, padding=CONFIG.PADDING)

    return padded_sequences

def create_model(learning_rate):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            CONFIG.VOCAB_SIZE,
            CONFIG.EMBEDDING_DIM,
            input_length=CONFIG.MAX_LENGTH
        ),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(
            16,
            activation='relu'
        ),
        tf.keras.layers.Dense(
            1,
            activation='sigmoid'
        )
    ])
    
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                  optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                  metrics=[
                      tf.keras.metrics.BinaryAccuracy(name='binary_accuracy'),
                      tf.keras.metrics.Precision(name='precision'),
                      tf.keras.metrics.Recall(name='recall')
                  ])
    
    return model

def train_model(model, features, output, epochs, batch_size, validation_split):
    history = model.fit(
        x=features,
        y=output,
        epochs=epochs,
        verbose=1,
        batch_size=batch_size,
        validation_split=validation_split
    )
    
    return history

def print_train_metrics(history: tf.keras.callbacks.History):
    plt.plot(
        history.epoch, 
        history.history['loss'], label='Loss'
    )
    plt.plot(
        history.epoch, 
        history.history['binary_accuracy'], label='Binary Accuracy'
    )
    plt.plot(
        history.epoch, 
        history.history['precision'], label='Precision'
    )
    plt.plot(
        history.epoch, 
        history.history['recall'], label='Recall'
    )

    plt.title('Evaluation metrics')
    plt.xlabel('Epoch')
    plt.legend()

    plt.savefig('./models/train_metrics.png')

def print_train_val_metrics(history: tf.keras.callbacks.History):
    pd.DataFrame(history.history).plot()
    plt.title("Evaluation metrics")

    plt.savefig('./models/train_val_metrics.png')

def main(file_name: str):
    df = pd.read_csv(f'./data/{file_name}_processed.csv')

    X = tokenize_text(df['text'])
    y = df['sentiment']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        shuffle=True,
        stratify=y,
        random_state=1,
        test_size=CONFIG.TEST_SPLIT
        )

    model = create_model(CONFIG.LEARNING_RATE)

    print('Training model...')
    history = train_model(model, X_train, y_train, CONFIG.EPOCHS_NUMBER, CONFIG.BATCH_SIZE, CONFIG.VALIDATION_SPLIT)

    print('Evaluating model...')
    model.evaluate(X_test, y_test)

    model.save("./models/model.keras")

    print_train_metrics(history, epochs)
    print_train_val_metrics(history)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.file_name)