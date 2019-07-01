
"""forth Test"""
"""
Author : HSKIM
Date : 190701
Target : Make all 
ver 1.0.1
comment :  패션의류 _ 여성트랜드 의류 (category2)

            
"""


# Path & ENV params

#cle = open('./ilotte_cleaned_test.txt', 'w')
from bs4 import BeautifulSoup as BS
import json
import requests
import urllib.request
import re
ilotte_json = open('./ilotte_json_2.json', 'w')
fileLocation = "./"

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
2. 아래의 URL은 lotteimall에서 패션의류/전체에 대하여 접근할 수 있는 url, header, data 양식이다.
3. lotteimall은 POST방식으로 요청하고 있다.
4. 카테고리는 패션의류 / 전체 , 여성브랜드의류, 여성트랜드의류, 진/유니섹스, 남성캐주얼, 남성정장셔츠
5. 지금이 코드는 롯데imall 베스트 100 - 패션의류 - 여성트랜드의류 부분이다.
"""

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
headers = {'Content-type': 'application/x-www-form-urlencoded'}
data = {"goods_rnk_sct_cd": "S",
        "goods_sum_sct_cd": "R3",
        "dpml_no": "1",
        "sum_disp_no": "5157020"}


def crawling_func(html):
    temp_list = []
    temp_dict = {}

    # tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    tr_list = html.select('li')

    for tr in tr_list:
        rank = tr.find('div').text.rstrip()
        title = tr.find('p', {'class': 'txt_name'}).find('a').get_text(strip=True).rstrip()
        img = tr.find('div', {'class': 'thumb'}).find('img').get('src')
        price = int(tr.find('span', {'class': 'price1'}).text.rstrip(
            '원\t').replace(',', ''))
        try:
            price2 = int(tr.find('span', {'class': 'price2'}).text.rstrip(
                '원\t').replace(',', ''))
        except AttributeError:
            price2 = None

        age = None
        temp_list.append({'rank': int(rank), 'title': title,
                          'img': img, 'price': price, 'price2': price2, 'age': age})

    return temp_dict, temp_list

# Cleaning Function.


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

    print("ilottemall crawling Start.....")
    # 단순 html파일 읽기.
    r = requests.post(ilottemall_url, data=data,
                      headers=headers, auth=None, allow_redirects=True)
    html = r.text
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    #print(soup, file=soup_debug)

    lotteTemp = crawling_func(soup)
    temp_list = lotteTemp[1]
    temp_dict = dict(temp_dict, **lotteTemp[0])
    print(makejson(temp_list), file=ilotte_json)


if __name__ == '__main__':
    main()
