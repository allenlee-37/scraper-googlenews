from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time

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

def get_title_body(number):
    '''
    1. get_keyword_news_url에서 얻은 리스트에서 number번째 기사를 열음
    2. 열은 기사에서 title과 body를 긁어옴
    3. title과 body를 반환
    '''
    url = url_list[number]
    media = media_list[number]
    # driver 실행
    driver = webdriver.Chrome('/Users/master/dev/PythonPr/news-crawler/chromedriver', chrome_options=options)
    driver.implicitly_wait(5)

    driver.get(url)
    driver.implicitly_wait(5)

    # 제목
    title = driver.find_element(By.CSS_SELECTOR, 'h1')
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    return title, paragraphs, url, media

def process_title_body(search_range = len(url_list)):
    result = []
    for i in tqdm(range(search_range)):
        try:
            title_elem, paragraphs, url, media = get_title_body(i)
            body=[]
            for elem in paragraphs:
                if len(elem.text) < 50: pass
                else: body.append(elem.text) 
            body = ' '.join(body)
            title = title_elem.text
            new_row = [title, body, media, url]
            result.append(new_row)
            print(new_row)
            if i%10==0:result.to_excel(f'{i}-news-crawl-result.xlsx')
        except:
            error_url = url_list[i]
            result.append(['error', 'error', 'error', error_url])
    return pd.DataFrame(result, columns=['title', 'body', 'media', 'url'])

result = process_title_body()
result.to_excel('news-crawl-result-test3.xlsx')