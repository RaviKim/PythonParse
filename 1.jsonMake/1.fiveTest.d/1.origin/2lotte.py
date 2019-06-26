
"""forth Test"""
"""
Author : HSKIM
Date : 190624
Target : lottedotcom Test
Difficult : Easy
ver 0.0.2
comment : lottedotcom Test
1) Check url for using.
2) added crawl func, added rank
BUG REPORT : 
    """
from bs4 import BeautifulSoup as BS
import json
import csv
import requests
import urllib.request
import re

# Path & ENV params

f = open('./lottedotcom_html_test.txt', 'w')
cle = open('./lottedotcom_cleaned_test.txt', 'w')
soup_debug = open('./soup_text.txt', 'w')
tr_html = open('./tr_html.txt','w')
fileLocation = "./"

"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
"""

lottedotcommall_url = 'http://www.lotte.com/display/viewRankingZoneMain.lotte?disp_no=5543628&disp_grp_nm=%ED%8C%A8%EC%85%98%EC%9D%98%26gt%3B+%EB%A5%98&upr_disp_no=&spick_disp_no=0&goods_sum_sct_cd=R0&goods_rnk_sct_cd=S&gen_sct_cd=A&age_sct_cd=20&dept_yn=&type=pc&tracking=RANKING_Sort_A_20#rankMiddle'
#Cleaning Function.
def crawling_func(html):
    temp_list = []
    temp_dict = {}

    #tr_list 는 가공되기 전의 상태입니다. 이걸 가공해야합니다.
    #tr_list = html.select('li')
    tr_list = html.select("[class~=opt01]")

    for tr in tr_list:

        try:
            rank = tr.find('div').find('p', {'class' : 'flag'}).find('img').get('alt')
            title = tr.find('div', {'class':'contents benefittit'}).find('a').find('p', {'class':'option threeLine'}).text
            img = tr.find('div').find('p', {'class' : 'flag'}).find('img').get('src')
            #print(rank,img, file= cle)
            price1 = tr.find('div', {'class':'price benefitsprice'}).find('span').text
            price2 = tr.find('div', {'class':'price benefitsprice'}).find('p', {'class':'goodbenefit'}).find('strong').text


        except AttributeError:
            rank = None
            title = None
            img = None
            price1 = None
            price2 = None

        except UnboundLocalError:
            rank = None
            title = None
            img = None
            price1 = None
            price2 = None
        #temp_list.append([rank, title, img, price1, price2])
        temp_dict[rank] = {'title' : title,'img' : img,  'price1':price1, 'price2':price2}

    return temp_dict
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
        print("lottedotcom crawling Start.....")
   # 단순 html파일 읽기.
        
        r = requests.get(lottedotcommall_url)
        html = r.text

        temp_list = []
        temp_dict = {}

    # 읽은 html파일 처리
        soup = BS(html, 'html.parser')
        print(soup, file=soup_debug)
        crawling_func(soup)

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
