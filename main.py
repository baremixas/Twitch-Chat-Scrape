from scrape import run_page, get_data

driver = run_page("lec", 5)

input()

data = get_data(driver)

print(data)
