import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Main script')

    parser.add_argument(
        '--stream_name', 
        type=str, 
        default='shroud',
        help='Twitch username'
    )
    parser.add_argument(
        '--delay', 
        type=float, 
        default=3, 
        help='Delay time in s to wait for page to load'
    )

    return parser.parse_args()

def run_page(twitch_username: str, delay: int):
    options = webdriver.ChromeOptions()
    options.add_argument("headless") #Run browser in background

    driver = webdriver.Chrome(options=options)

    driver.get(f'https://www.twitch.tv/popout/{twitch_username}/chat')

    #Wait for 5s for page to load
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
        message = text.find_element(By.XPATH, './/span[contains(@class, "text-fragment")]').get_attribute('innerHTML')
        data.append({'user':username, 'text':message})

    web_driver.quit()

    return data

def main(stream_name: str, delay: float):
    driver = run_page(stream_name, delay)

    input()

    data = get_data(driver)

    print(data)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.stream_name, args.delay)