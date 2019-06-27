
"""forth Test"""
"""
Author : HSKIM
Date : 190627
Target :    json Converter 
ver 0.0.2
comment :   Make Text File to Json format. 
            Oddconcepts style match.
"""
from bs4 import BeautifulSoup as BS
import json
import requests
import urllib.request
import re

# Path & ENV params

cle = open('./ilotte_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')
ilotte_json = open('./ilotte_json_1.json','w')
fileLocation = "./"
"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
2. 아래의 URL은 lotteimall에서 패션의류/전체에 대하여 접근할 수 있는 url, header, data 양식이다.
3. lotteimall은 POST방식으로 요청하고 있다.
4. 카테고리는 패션의류 / 전체 , 여성브랜드의류, 여성트랜드의류, 진/유니섹스, 남성캐주얼, 남성정장셔츠
"""

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
headers = {'Content-type':'application/x-www-form-urlencoded'}
data = {"goods_rnk_sct_cd": "L",
        "goods_sum_sct_cd": "R7",
        "dpml_no": "",
        "sum_disp_no": "10"}


def crawling_func(html):
    temp_list = []
    temp_dict = {}

    #tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    tr_list = html.select('li')

    for tr in tr_list:
        rank = tr.find('div').text.rstrip()
        title = tr.find('p', {'class':'txt_name'}).find('a').text.rstrip()
        img = tr.find('div', {'class':'thumb'}).find('img').get('src')
        price1 = int(tr.find('span', {'class':'price1'}).text.rstrip('원\t').replace(',', ''))
        try:
            price2 = int(tr.find('span', {'class':'price2'}).text.rstrip('원\t').replace(',', ''))
        except AttributeError:
            price2 = None

        temp_list.append([rank, title, img, price1, price2])
#        temp_dict[rank] = {'rank' :int(rank), 'title' : title, 'img' : img, 'price1':price1, 'price2':price2}
        temp_dict[rank] = {'rank' :int(rank), 'title' : title, 'img' : img, 'price1':price1, 'price2':price2}

    
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
    clean_text = re.sub('[\t]', '', text)
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
    r = requests.post(ilottemall_url, data=data, headers=headers, auth=None, allow_redirects=True)
    html = r.text
    temp_list = []
    temp_dict = {}
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    print(soup, file=soup_debug)
    temp_dict = dict(temp_dict, **crawling_func(soup))

    for item in temp_dict:
        print(item, temp_dict[item]['rank'], temp_dict[item]['title'], temp_dict[item]['img'],
              temp_dict[item]['price1'], temp_dict[item]['price2'], file=cle)
    #전송용
    #jsonString = json.dumps(temp_dict)
    """
    jsonString 인코딩시에 유니코드로 인코딩 되니까 신경써서 아래처럼 ensure_ascii부분 처리해야함
    """
    jsonString = json.dumps(temp_dict, indent=4, ensure_ascii=False)
    print(jsonString, file=ilotte_json)


if __name__ == '__main__':
    main()
