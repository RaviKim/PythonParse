from urllib.request import urlopen
from bs4 import BeautifulSoup

"""First Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy

"""
html = urlopen("http://www.lotteimall.com/display/sellRank100GoodsList.lotte")
bsObject = BeautifulSoup(html, "html.parser")



f = open('./lotteimall.txt', 'a')
temp = bsObject

print(temp, file = f)
f.close()


