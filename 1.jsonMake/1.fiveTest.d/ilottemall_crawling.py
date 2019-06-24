
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
#f = open('./parseTest.txt', 'w')
#n = open('./testText.txt', 'a')

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


#Text -> Json format converter
def readFiles(sFileLocation, sFromFileName):
    with open(sFileLocation + sFromFileName, mode="rt", encoding='utf-8') as f:
        stringList = f.readlines()
        item = stringList[0]
        print(item)

        for item in stringList:
            jsonObject = json.loads(item)
            print(jsonObject['TV'] + " ")


#Using Text crawl.
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
    
    #Create Text file
    open_ilotte_file = open(ilottemall_crawlText, 'w')
    #Url bring
    result_ilotte_file = get_text(ilottemall_url)

    #result File added
    open_ilotte_file.write(result_ilotte_file)

    #Make clean data.
    read_ilotte_file = open(ilottemall_crawlText, 'r')
    write_ilotte_file = open(ilottemall_output_text, 'w')
    ilottemall_text = read_ilotte_file.read()

    #re define clean data
    ilottemall_text = clean_text(ilottemall_text)
    write_ilotte_file.write(ilottemall_text)
    open_ilotte_file.close()
    read_ilotte_file.close()
    write_ilotte_file.close()

if __name__ == '__main__':
    main()
