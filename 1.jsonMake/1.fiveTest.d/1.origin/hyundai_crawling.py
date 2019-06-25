
"""forth Test"""
"""
Author : HSKIM
Date : 190620
Target :hyundai Test
Difficult : Easy
ver 0.0.1
comment : Hyundai Test
            1) Check url for using.

BUG REPORT : 
    Compare ilotte_mall , hyundai mall removed \n chracter.
    so must changed
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request
import re

# Path & ENV params

f = open('./hyundai_html_test.txt', 'w')
cle = open('./hyundai_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')

fileLocation = "./"

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
"""

hyundaimall_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?dispCsfGrpGbcd=01&mode=sell&sectId=1009&type=hmall&ajaxYn=Y&depth=4'

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
    r = requests.get(hyundaimall_url)
    html = r.text
    
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)


    titles = soup.select('div.raking.weekly') #Strong class
    for title in titles:
        print(title.text, file=f)
        print(clean_text(title.text), file=cle)

    
if __name__ == '__main__':
    main()
