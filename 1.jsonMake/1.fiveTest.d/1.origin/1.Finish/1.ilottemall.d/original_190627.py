
"""forth Test"""
"""
Author : HSKIM
Date : 190624
Target :    json Converter 
Difficult : Easy
ver 0.0.1
comment :   Make Text File to Json format. 
"""
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request
import re

# Path & ENV params

cle = open('./ilotte_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')

fileLocation = "./"

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
"""

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
#ilottemall_url = 'http://www.lotteimall.com/display/sellRank100.lotte?tlog=a1001_5#best100'



def crawling_func(html):
    temp_list = []
    temp_dict = {}

    #tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    tr_list = html.select('li')

    for tr in tr_list:
        rank = tr.find('div').text
        title = tr.find('p', {'class':'txt_name'}).text
        img = tr.find('div', {'class':'thumb'}).find('img').get('src')
        price1 = tr.find('span', {'class':'price1'}).text
        try:
            price2 = tr.find('span', {'class':'price2'}).text
        except AttributeError:
            price2 = None

        temp_list.append([rank, title, img, price1, price2])
        temp_dict[rank] = {'title' : title,'img' : img,  'price1':price1, 'price2':price2}

    return temp_dict

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

def tclen_text(text):
    clean_text = re.sub('[\t]','',text)
    return clean_text


def makejson(sFileLocation, sFromFileName):
    with open(sFileLocation + sFromFileName, mode="rt", encoding='utf-8')as f:
        stringlist = f.readlines()
        item = stringlist[0]
        print(item)

        for item in stringlist:
            jsonObject = json.loads(item)



def main():
    print("ilottemall crawling Start.....") 
    # 단순 html파일 읽기.
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    #data = {"data" : "goods_rnk_sct_cd=L&goods_sum_sct_cd=R7&dpml_no=&sum_disp_no=10"}   
    data = {"goods_rnk_sct_cd": "L",
            "goods_sum_sct_cd": "R7",
            "dpml_no": "",
            "sum_disp_no": "10"}

    r = requests.post(ilottemall_url, data =data, headers = headers, auth=None, allow_redirects=True )

    html = r.text

    temp_list = []
    temp_dict = {}

    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)


    """
    for title in titles:
        print(title.text, file=f)
        print(clean_text(title.text), file=cle)
        """

    temp_dict = dict(temp_dict, **crawling_func(soup))

    for item in temp_dict:
        print(item, temp_dict[item]['title'], temp_dict[item]['img'],  temp_dict[item]['price1'], temp_dict[item]['price2'], file=cle)

if __name__ == '__main__':
    main()
