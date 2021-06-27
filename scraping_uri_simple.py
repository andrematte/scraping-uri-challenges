# Import Libraries
import requests
import pandas as pd

from time import sleep

from tqdm import tqdm
from bs4 import BeautifulSoup 

def scrape_challenge(number):
    """
    scrape_challenge

    Function to scrape a single challenge information

    Args:
        number (int): Challenge number

    Returns:
        dict: Available challenge information
    """    
    url_index = f'https://www.urionlinejudge.com.br/repository/UOJ_{number}.html'

    page = requests.get(url_index)
    soup = BeautifulSoup(page.content, 'html.parser')

    info = {}

    info["Number"] = int(soup.body.find("span").get_text().split(" | ")[1])
    info["Title"] = soup.body.find("h1").get_text()
    info["URL"] = url_index
    info["Author"] = soup.body.find('p').get_text().replace('\n                    ', '').split(', ')[0]

    return info


# Variables to store data
challenges = []
failed = []

# Loop through all 3279 challenges
for i in tqdm(range(1000, 3279)):
    sleep(0.5)
    try:
        challenge_info = scrape_challenge(i)
        challenges.append(challenge_info)
    except:
        print(f'Failed to scrape challenge {i}')
        failed.append(i)
        

# Create and save dataframe
dataframe = pd.DataFrame(challenges)
dataframe = dataframe.set_index('Number')
dataframe.to_csv('uri_challenges_simple.csv')