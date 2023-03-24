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

def crawling(keyword):
    # 목표 url: 구글 뉴스
    url = 'https://news.google.com/home?hl=en-US&gl=US&ceid=US:en'
    # 크롬 드라이버 실행
    driver = webdriver.Chrome('/Users/master/dev/PythonPr/news-crawler/driver/chromedriver', chrome_options=options)
    driver.implicitly_wait(2)
    # url 가져오기
    driver.get(url)

    # 검색창 찾기: search_box
    search_box = driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/input[2]')
    # 검색어 입력: 1년간 결과 검색
    search_box.send_keys(f'"{keyword}" when:1y')
    # 검색창 클릭
    driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[2]/div[2]/form/button[4]').click()
    driver.implicitly_wait(3)

    # url의 리스트 만들기
    # 기사 요약 링크가 있는 div에서 출발해서 a 태그 끌고 온다. 
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
    driver = webdriver.Chrome('/Users/master/dev/PythonPr/news-crawler/driver/chromedriver', chrome_options=options)
    driver.implicitly_wait(2)
    try:
        # url 오픈
        driver.get(url)
        driver.implicitly_wait(5)
        # p 태그 찾기
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        driver.implicitly_wait(5)
        # 끌고온 문단의 리스트들: 문자열 길이가 50 이상이면 body 변수로 합쳐버린다.
        body = ''.join([test.text if len(test.text)>50 else '' for test in paragraphs])
        # article 변수로 저장한다. 본문은 url와 같은 순서로 리스트에 저장됨
        driver.quit()
    except:
        body = 'error body crawling'
        driver.quit()
    return body

def concat_body(keyword):
    urls, titles = crawling(keyword)
    article_body = []
    for url in tqdm(urls): # 테스트
        try: article_body.append(get_body(url))
        except: article_body.append('error in concat')

    # titles, urls, article 세가지 모두 합쳐야함
    crawl_result_list = [titles, article_body, urls]
    crawled_df = pd.DataFrame(crawl_result_list).transpose()
    crawled_df.columns = ['title', 'body', 'url']
    data_path = '/Users/master/dev/PythonPr/news-crawler/crawl_result'
    save_time = datetime.now()
    crawled_df.to_excel(f'{data_path}/{keyword}{save_time}.xlsx')
    return 

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--keyword', '-k', type=str, required=True)
    args = p.parse_args()
    concat_body(args.keyword)

if __name__ == '__main__':
    main()

'''
source .venvCrawler/bin/activate
python3 crawler2.py -k '
1. korean corn dog
2. korean recipe
3. kimchi
4. korean menu
''' 