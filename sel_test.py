from selenium import webdriver

driver = webdriver.Chrome('/Users/ravikim/Documents/chromedriver')

driver.implicitly_wait(3)
driver.get('https://google.com')
