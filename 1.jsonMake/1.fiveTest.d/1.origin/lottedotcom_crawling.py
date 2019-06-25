
"""forth Test"""
"""
Author : HSKIM
Date : 190624
Target : lottedotcom Test
Difficult : Easy
ver 0.0.1
comment : lottedotcom Test
            1) Check url for using.

BUG REPORT : 
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request
import re

# Path & ENV params

f = open('./lottedotcom_html_test.txt', 'w')
cle = open('./lottedotcom_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')

fileLocation = "./"

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
"""

lottedotcommall_url = 'http://www.lotte.com/display/viewRankingZoneMain.lotte?disp_no=5543628&disp_grp_nm=패션의류&upr_disp_no=&spick_disp_no=0&goods_sum_sct_cd=P0&goods_rnk_sct_cd=S&gen_sct_cd=A&age_sct_cd=A&dept_yn=&type=pc&tracking=RANKING_GCB_01#rankMiddle'
#Cleaning Function.

def clean_text(text):
    """
    <parameter> : text value
    <Return> : removed space and return cleaned text file.
    """
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          ' ', cleaned_text)
    # 공백을 삭제하는 코드.
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text


def main():
    print("ilottemall crawling Start.....") 
    # 단순 html파일 읽기.
    r = requests.get(lottedotcommall_url)
    html = r.text
    
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)


    titles = soup.select('div.contents.benefittit') #Strong class
    for title in titles:
        print(title.text, file=f)
        print(clean_text(title.text), file=cle)

    
if __name__ == '__main__':
    main()
