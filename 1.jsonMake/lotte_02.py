import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import os


"""First Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy
ver :  0.2
Target : requests, Beautiful soup Used

"""

""" Python File's location"""
#BASE_DIR = os.path.dirname(os.path.abspath('Users/ravikim/crl/1.code'))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://www.lotteimall.com/display/sellRank100GoodsList.lotte')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    'li > a'
)
"""
Copy selector
#rn2th_container > div > div.container_best > div.area_product_list > ul > li:nth-child(1) > div.thumb > a
"""
data = {}

for title in my_titles:
    data[title.text] = title.get('alt')

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)

with open(os.path.join(BASE_DIR, 'originData.html'), 'w+') as html_file:
    json.dump(data, soup)

print("end")
