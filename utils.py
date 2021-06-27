# Utility Functions for the URI Scraping Project
import requests
import pandas as pd

from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup


def get_problem_urls():
    problem_urls = []

    problems_xml = requests.get('https://www.urionlinejudge.com.br/judge/problems/sitemap.xml')
    soup = BeautifulSoup(problems_xml.text, 'html.parser')
    
    for url in soup.findAll('url'):
        problem_urls.append(url.get_text()[:-20])

    problem_urls = [item.replace('en','pt') for item in problem_urls]
    return problem_urls


def scrape_problem_urls(driver, problem_urls, sleep_timer=0.5):
    problems_data = []
    failed = []

    for problem_url in tqdm(problem_urls):
        sleep(sleep_timer)
        try:
            driver.get(problem_url)
            info = {}

            info['Number'] = problem_url[-4:]
            info['Class'] = driver.find_element_by_xpath('//*[@id="page-name-c"]/ul/li[1]').text
            info['Level'] = driver.find_element_by_xpath('//*[@id="page-name-c"]/ul/li[3]/strong').text
            info['Points'] = driver.find_element_by_xpath('//*[@id="page-name-c"]/ul/li[5]/em').text
            info['URL'] = problem_url
            
            driver.get(f'https://www.urionlinejudge.com.br/repository/UOJ_{info["Number"]}.html')
            
            info['Title'] = driver.find_element_by_xpath('/html/body/div[1]/h1').text

            problems_data.append(info)
        
        except:
            failed.append(problem_url)
            
    return problems_data, failed


def create_dataframe(problem_data):
    columns = ['Number', 'Class', 'Title', 'Level', 'Points', 'URL']
    problem_df = pd.DataFrame(problem_data)
    problem_df = problem_df[columns]

    problem_df['Level'] = problem_df['Level'].str.replace('NÍVEL ','')
    problem_df['Points'] = problem_df['Points'].str.replace(' PONTOS','')
    problem_df['Points'] = problem_df['Points'].str.replace(' POINTS','')
    problem_df['Points'] = problem_df['Points'].str.replace('\+ ','', regex=True).astype('float')

    return problem_df