from selenium import webdriver
from bs4 import BeautifulSoup as bs

"""First Test"""
"""
Author : HSKIM
Date : 190618
Target : lotteimall
Difficult : Easy

"""

# Path params
chromedriver_path = '/Users/ravikim/Documents/chromedriver'
url = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'

#

options = webdriver.ChromeOptions()
# Open browsers not popuped
options.add_argument('headless')

#driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
driver = webdriver.Chrome(chromedriver_path)
driver.get(url)
#print(driver.page_source)

soup = bs(driver.page_source, "html.parser")
"""
body > li:nth-child(2) > div.thumb > a > img
#rn2th_container > div > div.container_best > div.area_product_list > ul > li:nth-child(1) > div.thumb > a > img
"""
#article_table = soup.select("div.area_product_list img")
article_table = soup.select("li a")
print(article_table)

#driver.quit()
#article_list = article_table.get_attribute("strong")
#article_list = article_table.select("strong")
#print(article_list)
"""
for article in article_list:
    try:
        number = article.select(".list-count")[0].get_text()
        subject = article.select(".board-list a")[0].get_text()

    except:
        pass
"""
"""headless test to do..."""

for title in article_table:
    print(title.text)
    print(title.get('strong'))

driver.quit()
