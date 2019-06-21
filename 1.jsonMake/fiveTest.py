"""forth Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy
ver 0.0.5
comment : 1. img url 가져오는 것 구현.
          2. json 파일로 만드는 것 구현
          3. 환경변수 최대한 이용할 것
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request

# Path & ENV params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
f = open('./parseTest.txt', 'w')
n = open('./testText.txt', 'a')

ilottemall_crawlText = 'ilottemall_crawlText.txt'
hyundaihmall_crawlText = 'hyungdaihmall_crawlText.txt'
lottedotcom_crawlText = 'lottedotcom_crawlText.txt'

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
hyungdaihmall_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?dispCsfGrpGbcd=01&mode=sell&sectId=168445&type=hmall&ajaxYn=Y&depth=3'
lottedotcom_url = 'http://www.lotte.com/display/viewRankingZoneMain.lotte?disp_no=5543628&disp_grp_nm=%ED%8C%A8%EC%85%98%EC%9D%98%EB%A5%98&upr_disp_no=&spick_disp_no=0&goods_sum_sct_cd=P0&goods_rnk_sct_cd=S&gen_sct_cd=A&age_sct_cd=A&dept_yn=&type=pc&tracking=RANKING_Sort_A_A#rankMiddle'

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
    tr_list = html.select('body li')
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


ilotte_list = []
ilotte_dict = {}

req = requests.get(url)
html = req.text
soup = BS(html, 'html.parser')
ilottemall_crawling(soup)


toCSV(ilotte_list)
toJson(ilotte_dict)

def get_text(URL):
    """
    get text file function.
    Just test.
    """
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BS(source_code_from_URL, 'html.parser', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('li'):
        text = text + str(item.find_all(text=True))
    return text

def main():
    open_ilotte_file = open(ilottemall_crawlText, 'w')
    open_hyungdai_file = open(hyundaihmall_crawlText, 'w')
    open_lottedotcom_file = open(lottedotcom_crawlText, 'w')

    result_ilotte_file = get_text(ilottemall_url)
    result_hyungdai_file = get_text(hyungdaihmall_url)
    result_lottedotcom_file = get_text(lottedotcom_url)

    open_ilotte_file.write(result_ilotte_file)
    open_hyungdai_file.write(result_hyungdai_file)
    open_lottedotcom_file.write(result_lottedotcom_file)

    open_ilotte_file.close()
    open_hyungdai_file.close()
    open_lottedotcom_file.close()

if __name__ == '__main__':
    main()
