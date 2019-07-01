
"""forth Test"""
"""
Author : HSKIM
Date : 1907019
Target :    json Converter 
ver 1.0.0
comment : lottedotcom _ crawl all data. 
verData : 1.0.0 make origin crawl. 
"""

# Path & ENV params

from bs4 import BeautifulSoup as BS
import json
import requests
import urllib.request
import re
de = open('./debug.html', 'w')
lottedot_json = open('./lottedot_json_FE_1.json', 'w')
fileLocation = "./"
"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
2. 아래의 URL은 lottedotmall방식이다. 
3. lottedotimall은 GET방식으로 요청하고 있다.
4. Category : 전체 , 20대 , 30대 , 40대 , 50대 이상 , 여자 - 20, 30, 40, 50대 이상, 남자 - 20,30,40,50대 이상 
"""

lottedotmall_url = 'http://www.lotte.com/display/viewRankingZoneMain.lotte?disp_no=5543628&disp_grp_nm=%ED%8C%A8%EC%85%98%EC%9D%98%EB%A5%98&upr_disp_no=&spick_disp_no=0&goods_sum_sct_cd=R0&goods_rnk_sct_cd=S&gen_sct_cd=F&age_sct_cd=20&dept_yn=&type=pc&tracking=RANKING_Sort_F_20#rankMiddle'


def crawling_func(html):
    temp_list = []
    temp_dict = {}

    # tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    tr_list = html.select(
        'div.best30_cont.renewBest > div.third > ul > li.opt01 > div.cont > ol > li')
    for tr in tr_list:
        rank = tr.find('div', {'class': 'produnit prd_170v'}).find(
            'p', {'class': 'flag'}).find('img').get('alt').lstrip('rank')
        title = tr.find('div', {'class': 'info_zone'}).find(
            'div', {'class': 'contents benefittit'}).find('a').find('p').text
        img = tr.find('div', {'class': 'produnit prd_170v'}).find(
            'div', {'class': 'photo_zone'}).find('img').get('src')
        try:
            price = tr.find('div', {'class': 'info_zone'}).find('div', {
                'class': 'price benefitsprice'}).find('p').find('span').text.rstrip('원').replace(',', '')
            price2 = None
        except AttributeError:
            price = tr.find('div', {'class': 'info_zone'}).find('div', {'class': 'price benefitsprice'}).find(
                'p', {'class': 'goodbenefit'}).find('strong').text.rstrip('원').replace(',', '')
            price2 = tr.find('div', {'class': 'info_zone'}).find('div', {
                'class': 'price benefitsprice'}).find('p').find('del').text.rstrip('원').replace(',', '')

        age = '20'
        temp_list.append({'rank': int(rank), 'title': title,
                          'img': img, 'price': price, 'price2': price2, 'age': age})
        print(temp_list, file=de)
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

    print("lottedotmall crawling Start.....")
    # 단순 html파일 읽기.
    r = requests.get(lottedotmall_url)
    html = r.text
    # 읽은 html파일 처리
    soup = BS(html, 'html.parser')
    #print(soup, file=soup_debug)
    lottedotTemp = crawling_func(soup)
    temp_list = lottedotTemp[1]
    temp_dict = dict(temp_dict, **lottedotTemp[0])
    print(makejson(temp_list), file=lottedot_json)


if __name__ == '__main__':
    main()
