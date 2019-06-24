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
          4. json Added
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
hyundaihmall_crawlText = 'hyundaihmall_crawlText.txt'
lottedotcom_crawlText = 'lottedotcom_crawlText.txt'

ilottemall_output_text = 'ilottemall_output_text.txt'
hyundaihmall_output_text = 'hyundaihmall_output_text.txt'
lottedotcom_output_text = 'lottedotcom_output_text.txt'


"""
1. URL 부분은 언제든지 변경이 되어질 수 있다.
2. hyundaihmall_과 lottedotcom은 상세 카테고리마다 url이 달라지므로 1차적 분석 이후 자동화로 등록이 가능한지 여부를 확인한 뒤에, 그부분이 불가하다면 일일이 넣는 수밖에 없다. 그부분은 향후 고려를 진행한다.

"""

ilottemall_url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
hyundaihmall_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?dispCsfGrpGbcd=01&mode=sell&sectId=1009&type=hmall&ajaxYn=Y&depth='
#hyundaihmall_url = 'http://www.hyundaihmall.com/front/dpd/wkBestTypeTot.do?dispCsfGrpGbcd=01&mode=sell&sectId=168445&type=hmall&ajaxYn=Y&depth=3'
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
    open_hyundai_file = open(hyundaihmall_crawlText, 'w')
    open_lottedotcom_file = open(lottedotcom_crawlText, 'w')
    #Url bring
    result_ilotte_file = get_text(ilottemall_url)
    result_hyundai_file = get_text(hyundaihmall_url)
    result_lottedotcom_file = get_text(lottedotcom_url)

    #result File added
    open_ilotte_file.write(result_ilotte_file)
    open_hyundai_file.write(result_hyundai_file)
    open_lottedotcom_file.write(result_lottedotcom_file)
    
    #readFiles(fileLocation, "ilottemall_crawlText.txt")

    #Make clean data.
    read_ilotte_file = open(ilottemall_crawlText, 'r')
    read_hyundai_file = open(hyundaihmall_crawlText, 'r')
    read_lottedotcom_file = open(lottedotcom_crawlText, 'r')

    write_ilotte_file = open(ilottemall_output_text, 'w')
    write_hyundai_file = open(hyundaihmall_output_text, 'w')
    write_lottedotcom_file = open(lottedotcom_output_text, 'w')

    ilottemall_text = read_ilotte_file.read()
    hyundai_text = read_hyundai_file.read()
    lottedotcom_text = read_lottedotcom_file.read()

    ilottemall_text = clean_text(ilottemall_text)
    hyundai_text = clean_text(hyundai_text)
    lottedotcom_text = clean_text(lottedotcom_text)

    write_ilotte_file.write(ilottemall_text)
    write_hyundai_file.write(hyundai_text)
    write_lottedotcom_file.write(lottedotcom_text)

    open_ilotte_file.close()
    open_hyundai_file.close()
    open_lottedotcom_file.close()

    read_ilotte_file.close()
    read_hyundai_file.close()
    read_lottedotcom_file.close()

    write_ilotte_file.close()
    write_hyundai_file.close()
    write_lottedotcom_file.close()
if __name__ == '__main__':
    main()
