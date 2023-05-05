import requests
import pandas as pd
import numpy as np
import folium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(execute_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

df = pd.read_csv('상권정보_용산구.csv')
df['keyword'] = df['상호명'].map(str) + " " + df['도로명주소']
df['naver_map_url'] = ''
df['data-cid'] = ''

new_df = df[['상호명', '도로명주소']]

for i, keyword in enumerate(df['keyword'].tolist()):
    print("이번에 찾을 키워드: ", i, f"/{df.shape[0]} 행", keyword)
    try:
        # 검색 url 만들기
        naver_map_search_url = f'https://map.naver.com/v5/search/{keyword}/place'
        driver.get(naver_map_search_url)  # 검색 url 접속 = 검색하기
        time.sleep(4)  # 중요

        cu = driver.current_url  # 검색이 성공된 플레이스에 대한 개별 페이지
        res_code = re.findall(r"place/(\d+)", cu)
        final_url = 'https://pcmap.place.naver.com/restaurant/' + \
            res_code[0]+'/review/visitor#'

        print(final_url)
        df['data-cid'][i] = res_code
        df['naver_map_url'][i] = final_url

    except IndexError:
        df['naver_map_url'][i] = ''
        print('none')

    df.to_csv('소상공인_url.csv', encoding='utf-8-sig')
