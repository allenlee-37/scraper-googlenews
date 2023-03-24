from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm

'''keyword 설정'''
keyword = 'Korean food'

# Headless로 실행
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

def get_keyword_news_url(keyword):
    '''
    1. Google news에서 keyword 결과값을 검색
    2. 검색한 기사 결과의 url을 리스트로 반환
    '''   
    # 목표 url: 구글 뉴스
    url = 'https://news.google.com/home?hl=en-US&gl=US&ceid=US:en'
    # 크롬 드라이버 실행
    driver = webdriver.Chrome('/Users/master/dev/PythonPr/news-crawler/chromedriver')
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

    # 각 기사 element 가져오기
    articles = driver.find_element(By.CSS_SELECTOR, '#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb')
    paper_names = articles.find_elements(By.CSS_SELECTOR, 'div.wsLqz.RD0gLb > a')
    # anchor tag 가져오기
    anchors = articles.find_elements(By.TAG_NAME, 'a')

    # anchor에서 href 가져와서 list append
    url_list = []
    for anchor in anchors:
        url_list.append(anchor.get_attribute('href'))
    
    # 신문사 이름 가져오기
    media_list = []
    for paper in paper_names:
        if len(paper.text) < 3: pass
        else: media_list.append(paper.text)

    # 유니크한 url만 가져오기
    url_list = list(set(url_list))
    url_list.remove(None)
    return url_list, media_list

url_list, media_list = get_keyword_news_url(keyword)
