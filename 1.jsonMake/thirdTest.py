from selenium import webdriver
from bs4 import BeautifulSoup as bs

"""third Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy
ver 0.0.3
Comment : 이름 자체를 가져오는 것은 ver 0.0.2까지에서 확인되어짐
          0.0.3 에서는 가격정보와 다른 기타 정보들을 가져오는 것을 테스트 해봐야함.
"""

# Path params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'
f = open('./parseTest.txt', 'a')

options = webdriver.ChromeOptions()
# Open browsers not popuped
options.add_argument('headless')
driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
driver.get(url)

soup = bs(driver.page_source, "html.parser")
"""
Copy selector :Title 
이름 정보 가져오기
body > li:nth-child(1) > p.txt_name > a

"""
article_table = soup.select("li a")
art = open('./article_table.txt', 'w')
print(article_table,file = art)
"""
Copy selector : price 정보 가져오기
body > li:nth-child(1) > p.txt_price > span.price1
"""
price_table = soup.select("li span")
t = open('./price_table.txt', 'w')
print(price_table,file=t)

for title in article_table:
    print(title.text,file =f)

for price in price_table:
    print(price.text, file=t)


f.close()
t.close()
art.close()

driver.quit()
