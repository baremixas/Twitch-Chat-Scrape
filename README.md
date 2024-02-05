# Twitch Chat Scrape

The app was created using Python. Main goal was to improve knowledge about creating NLP machine learning models and data scraping.

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Launch](#launch)
* [Screens](#screens)
* [License](#license)

## General info

### Data Scrape

As Twitch.tv platform doesn't provide intuitive API, the idea was to use selenium package in Python in order to scrape data from live chat.

The code allows to run the browser with chat in window or headless mode. This allows user to decide whether it is usefull/necessary to have insight into current state of the chat.

### Dataset

To train the ML model, Sentiment140 dataset was chosen. Although old (2010), it is the biggest dataset of this type as it consists of 1.6 million tweets with Positive/Negative annotations. Unfortunately the dataset doesn't provide Neutral annotations, so the results can be not always valid or objective.

## Setup

During development process, Python 3.11.4 version was used.

It is recommended to create new virtual environment

```bash
python -m venv .venv
```

and activate it:

```bash
. .venv\Scripts\activate
```

To run the project you need to install required packages, which are included in `requirements.txt` file

```bash
pip install -r requirements.txt
```

## Launch

To launch the project you can run pipeline using:

```bash
sh scripts/run_pipeline.sh "my_data" "my_model" "xqc" 2 0 "my_texts" "my_results"
```

Arguments in order:
1. data_filename - name that will be given to downloaded dataset file - string
2. model_name - name that will be given to created ml model - string
3. stream_name - name of the stream, that will launch twitch.tv/stream_name chat - string
4. delay - delay in seconds, that pauses program to wait for page to load - float
5. headless - bool value determining headless/windowed browser mode - int (0/1)
6. texts_filename - name that will be given to scraped texts file - string
7. results_filename - name that will be given to results file - string

Each of the files can also be run independently, e.g.:

```bash
python src/data_ingestion.py --data_filename="my_data"
```

```bash
python src/model_training.py --data_filename="my_data" --model_name="my_model"
```

```bash
python src/scrape_text.py --stream_name="xqc" --delay=2 --headless=0 --texts_filename="my_texts"
```

```bash
python src/classify_text.py --model_name="my_model" --texts_filename="my_texts" --results_filename="my_results"
```

## Screens

## License
This project is licensed under the terms of **the MIT license**.
You can check out the full license [here](./LICENSE)
