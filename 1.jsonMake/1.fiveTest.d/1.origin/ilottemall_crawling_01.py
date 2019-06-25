
"""forth Test"""
"""
Author : HSKIM
Date : 190620
Target : ilottemall_url Test
Difficult : Easy
ver 0.0.6
comment : 1. Test two differ type code. what is more performance to transplant different code.
           1-1) First check def ilottemall_crawling(html)
           1-2) Test get_text - read Files 
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request
import re

# Path & ENV params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'

f = open('./ilotte_html_test.txt', 'w')
#n = open('./functionCheck.txt', 'w')
#html_debug = open('./html_text.txt', 'w')
soup_debug = open('./soup_text.txt','w')

fileLocation = "./"

ilottemall_crawlText = 'ilottemall_crawlText.txt'

ilottemall_output_text = 'ilottemall_output_text.txt'

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
"""

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'

#Crawling Function
def ilottemall_crawling(html):
    """
    ilottemall crawling 을 진행하는 함수입니다.
    기타 다른 사이트의 경우 별도의 함수를 만들어서 진행할 예정입니다.
    """
    temp_list = []
    temp_dict = {}
    #정보 가져오기
   # tr_list = html.select('body > li > p > a')
    tr_list = html.select('li')
    print(tr_list, file = n)
    for tr in tr_list:
        ranktop = tr.select('rank top')
        rank = tr.select('rank')
        """body > li:nth-child(1) > div.thumb > a > img"""
        img = tr.select('div', {'class':'thumb'}).find('a').find('img')['src']
        img = tr.find('div', {'class':'thumb'}).find('a').find('img').get('src')
        title = tr.select('.txt_name')
        price1 = tr.find('p', {'class':'txt_price'}).find('span', {'class':'price1'}).find('strong').text
        price2 = tr.find('p', {'class':'txt_price'}).find('span', {'class':'price2'}).find('strong').text
        temp_list.append([ranktop, rank, img, title, price1, price2])
        temp_dict[str(rank)] = {'img':img, 'title':title, 'price1':price1, 'price2':price2}

    return temp_list, temp_dict

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
    r = requests.get(ilottemall_url)
    html = r.text
    #html_debug = open('./html_text.txt', 'w')
    #print(html, file=html_debug)
    
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)

    """
    titles = soup.select('.txt_name') #Strong class
    for title in titles:
        print(title.text, file=f)
    """

    titles = soup.select('li') #Strong class
    for title in titles:
        print(title.text, file=f)

    
if __name__ == '__main__':
    main()
