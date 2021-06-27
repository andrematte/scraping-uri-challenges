# Import Libraries
import pandas as pd
from utils import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# WebDriver configuration
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Scraping Workflow
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

problem_urls = get_problem_urls()
problem_data, failed = scrape_problem_urls(driver, problem_urls, sleep_timer=0.3)
problem_df = create_dataframe(problem_data)

problem_df.to_csv('uri_challenges_complete.csv', index=False)

driver.quit()
