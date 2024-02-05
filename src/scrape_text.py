import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(description='Main script')

    parser.add_argument(
        '--stream_name', 
        type=str, 
        default='xqc',
        help='Twitch username'
    ),
    parser.add_argument(
        '--delay', 
        type=float, 
        default=3, 
        help='Delay time in s to wait for page to load'
    ),
    parser.add_argument(
        '--headless',
        type=lambda x: bool(int(x)),
        default=False,
        help='Headless mode (run browser in background)'
    ),
    parser.add_argument(
        '--texts_filename', 
        type=str, 
        default='texts', 
        help='Texts file name'
    )

    return parser.parse_args()

def run_page(twitch_username: str, delay: int, headless: bool):
    options = webdriver.ChromeOptions()
    
    if headless:
        options.add_argument("headless") #Run browser in background

    driver = webdriver.Chrome(options=options)

    driver.get(f'https://www.twitch.tv/popout/{twitch_username}/chat')

    time.sleep(delay)

    return driver


def get_data(web_driver):
    #Get all chat info
    element = web_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/section/div/div[4]/div[2]/div[2]/div[3]/div/div')

    try:
        texts = element.find_elements(By.XPATH, './div[contains(@class, "chat-line__message")]')
    except: texts = []

    data = []

    for text in texts:
        username = text.get_attribute('data-a-user')
        print(text.find_element(By.XPATH, './/span[contains(@class, "text-fragment")]').get_attribute('innerHTML'))
        message = text.find_element(By.XPATH, './/span[contains(@class, "text-fragment")]').get_attribute('innerHTML')

        data.append({'user': username, 'text': message})

    web_driver.quit()

    return data

def save_texts(data: list, texts_filename: str):
    with open(f'./data/{texts_filename}.csv', 'w', newline='', encoding="utf-8") as text_file:
        dict_writer = csv.DictWriter(text_file, data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main(stream_name: str, delay: float, headless: bool, texts_filename: str):
    driver = run_page(stream_name, delay, headless)

    input()

    data = get_data(driver)
    save_texts(data, texts_filename)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.stream_name, args.delay, args.headless, args.texts_filename)