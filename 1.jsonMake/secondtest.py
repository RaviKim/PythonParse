from selenium import webdriver
from bs4 import BeautifulSoup as bs

"""First Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy
ver 0.0.2
Comment : modified none data
"""

# Path params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'

options = webdriver.ChromeOptions()
# Open browsers not popuped
options.add_argument('headless')

driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
driver.get(url)

soup = bs(driver.page_source, "html.parser")
"""
Copy selector : 
body > li:nth-child(1) > p.txt_name > a
"""
article_table = soup.select("li a")
f = open('./parseTest.txt', 'a')

for title in article_table:
    print(title.text,file =f)

f.close()
driver.quit()
