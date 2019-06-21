"""forth Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy
ver 0.0.4.1
comment : 1. img url 가져오는 것 구현.
          2. json 파일로 만드는 것 구현
          3. Hyungdai mall added
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests

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
    tr_list = html.select('body strong')
    for tr in tr_list:
        ranktop = int(tr.find('div', {'class':'rank top'}))
        rank = int(tr.find('div', {'class':'rank'}))
        """body > li:nth-child(1) > div.thumb > a > img"""
        img = tr.find('div', {'class':'thumb'}).find('a').find('img')['src']
        img = tr.find('div', {'class':'thumb'}).find('a').find('img').get('src')
        title = tr.find('p', {'class':'txt_name'}).find('a').find('strong').text
        price1 = tr.find('p', {'class':'txt_price'}).find('span', {'class':'price1'}).find('strong').text
        price2 = tr.find('p', {'class':'txt_price'}).find('span', {'class':'price2'}).find('strong').text
        temp_list.append([ranktop, rank, img, title, price1, price2])
        temp_dict[str(rank)] = {'img':img, 'title':title, 'price1':price1, 'price2':price2}

    return temp_list, temp_dict

def hyundaimall_crawling(html):
    """
    hyundaimall crawling을 진행하는 함수입니다.
    해당 사이트의 문제는, 여성브랜드의류, 여성 트렌드, 홈쇼핑 여성의류, 남성브랜드 등 세분화가 되어진 점이며, 각자의 데이터 정보가 상이하다는 문제로 한번에 크롤링을 효율적으로 할 수 있는 방안을 생각해야합니다.
    """
    temp_list = []
    temp_dict = {}

    #정보가져오기
    #tr_list : body > div.raking.weekly > ul > li> a > span 
    tr_list = html.select('body span')
    for tr in tr_list:
        rank = int(tr.find('div', {'class':'em'}).find("rank-number"))
        img = tr.find('li', {'class': 
        img = tr.find('li', {'
        title = 
        price = 



#CSV Function
def toCSV(article_list):
    with open('article_table.csv', 'w', encoding='utf-8', newline='') as file:
        csvfile = csv.writer(file)
        for row in article_list:
            csvfile.writerow(row)

#Json Function
def toJson(article_dict):
    with open('article_dict.json', 'w', encoding='utf-8') as file:
        json.dump(article_dict, file, ensure_ascii=False, indent='\t')


# Path params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
hyungdai_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?_IC_=tab6#hisloc'



f = open('./parseTest.txt', 'a')
n = open('./testText.txt', 'a')
ilotte_list = []
ilotte_dict = {}

req = requests.get(url)
html = req.text
print(html, file=n)
soup = BS(html, 'html.parser')
print(soup, file=f)

for page in [1,2]:
    req = requests.get('http://www.lotteimall.com/chart/TOP100')
    html = BS(req.text, 'html.parser')
    
    print(ilottemall_crawling(html))
    ilotte_temp = ilottemall_crawling(html)
    ilotte_list += ilotte_temp[0]
    ilotte_dict = dict(ilotte_dict, **ilotte_temp[1])

for item in ilotte_list:
    print(item)

for item in ilotte_dict:
    print(item, ilotte_dict['img'], ilotte_dict['title'], ilotte_dict['price1'], ilotte_dict['price2'])

toCSV(ilotte_list)
toJson(ilotte_dict)
