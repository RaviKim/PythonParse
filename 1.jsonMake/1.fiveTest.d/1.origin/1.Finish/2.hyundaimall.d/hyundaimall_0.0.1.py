
"""forth Test"""
"""
Author : HSKIM
Date : 190628
Target :    json Converter 
ver 0.0.1
comment :   Make Text File to Json format. 
            Oddconcepts style match.
            Hyundaimall
"""
from bs4 import BeautifulSoup as BS
import json
import requests
import urllib.request
import re

# Path & ENV params

cle = open('./hyundai_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')
hyundai_json = open('./hyundai_json_1.json','w')
fileLocation = "./"
"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
2. 아래의 URL은 hyundaimall방식이다. 
3. hyundaiimall은 GET방식으로 요청하고 있다.
4. 카테고리는 패션의류 / 전체 , 여성브랜드의류, 여성트랜드의류, 진/유니섹스, 남성캐주얼, 남성정장셔츠
"""

hyundaimall_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?dispCsfGrpGbcd=01&mode=sell&sectId=1009&type=hmall&ajaxYn=Y&depth=' 

def crawling_func(html):
    temp_list = []
    temp_dict = {}

    #tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    tr_list = html.select('div.raking.weekly')
    #print(tr_list, file=cle)
    for tr in tr_list:
        rank = tr.find('em').text
        title = tr.find('span', {'class':'item-name'}).text.rstrip()
        img = tr.find('span', {'class':'pdtImg2'}).find('img').get('src')
        price = int(tr.find('span', {'class':'item-price'}).find('strong').text.replace(',', ''))
        price2 = None

        temp_list.append({'rank' :int(rank), 'title' : title, 'img' : img, 'price':price, 'price2':price2})

        print(temp_list, file=cle)
    return temp_dict, temp_list

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
    clean_text = re.sub('[\t]', '', text)
    return clean_text


def makejson(temp):
    jsonString = json.dumps(temp, indent=4, ensure_ascii=False)
    return jsonString


def main():
    temp_list = []
    temp_dict = {}
    
    print("hyundaimall crawling Start.....")
    # 단순 html파일 읽기.
    r = requests.get(hyundaimall_url)
    html = r.text
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)
    hyundaiTemp = crawling_func(soup)
    temp_list = hyundaiTemp[1]
    temp_dict = dict(temp_dict, **hyundaiTemp[0])

    for item in temp_dict:
        print(item, temp_dict[item]['rank'], temp_dict[item]['title'], temp_dict[item]['img'],
              temp_dict[item]['price'], temp_dict[item]['price2'], file=cle)
    #전송용
    #jsonString = json.dumps(temp_dict)
    """
    jsonString 인코딩시에 유니코드로 인코딩 되니까 신경써서 아래처럼 ensure_ascii부분 처리해야함
    """
    print(makejson(temp_list), file=hyundai_json)

if __name__ == '__main__':
    main()
