import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime

# Headless로 실행
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

def get_target_url(keyword):
    # 구글 뉴스에 뜨는 url을 가져올 예정
    # 해외 뉴스를 가져오는 것이 목표: en버전으로 가져옴
    url = 'https://news.google.com/home?hl=en-US&gl=US&ceid=US:en'
    # 드라이버 실행
    driver = webdriver.Chrome('./driver/chromedriver', chrome_options=options)
    driver.implicitly_wait(2)
    driver.get(url)
    driver.implicitly_wait(2)

    # 검색창 찾기
    search_box = driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/input[2]')
    # 검색박스에 키워드와 검색 기간 (1년)을 보낸다.
    search_box.send_keys(f'"{keyword}" when:1y')
    # 검색 클릭
    driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[2]/div[2]/form/button[4]').click()
    driver.implicitly_wait(3)

    # url 리스트 만들기
    url_list = driver.find_elements(By.XPATH, '//div[@class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]/a')
    urls = [url_elem.get_attribute('href') for url_elem in url_list] # href attribute를 가져온다.
    print(f'url 개수: {len(urls)}') 

    # 기사 제목의 리스트 만들기
    # url을 끌고 온 div와 같은 위치에서 출발해서 h3을 끌고 온다.
    title_list = driver.find_elements(By.XPATH, '//div[@class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]/div[1]/article/h3')
    titles = [title_elem.text for title_elem in title_list] # text attribute를 가져온다. 
    print(f'title 개수: {len(titles)}') 
    driver.quit()
    return urls, titles

def get_body(url):
    driver = webdriver.Chrome('./driver/chromedriver', chrome_options=options)
    driver.implicitly_wait(2)
    try: 
        driver.get(url)
        driver.implicitly_wait(5)
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        driver.implicitly_wait(2)
        body = ''.join([paragraph.text if len(paragraph.text)>50 else '' for paragraph in paragraphs])
    except: body = 'error body crawling'
    driver.quit()
    return body

def get_body_list(urls):
    body_list = []
    for url in tqdm(urls):
        try: body_list.append(get_body(url))
        except: body_list.apend('error in concat')
    return body_list

def make_dataFrame(titles, body_list, urls):
    crawl_result_list = [titles, body_list, urls]
    crawled_df = pd.DataFrame(crawl_result_list).transpose()
    crawled_df.columns = ['title', 'body', 'url']
    return crawled_df
    

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--keyword', '-k', type=str, required=True)
    args = p.parse_args()

    urls, titles = get_target_url(args.keyword)
    body_list = get_body_list(urls)
    result = make_dataFrame(titles, body_list, urls)

    data_path = './crawl_result'
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d")
    result.to_excel(f'{data_path}/{args.keyword}-{date_time_str}-result.xlsx')

if __name__ == '__main__':
    main()