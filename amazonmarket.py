import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = "https://www.amazon.com/"
search_word = str(raw_input("Enter your search word:\n"))


driver = webdriver.Firefox()
driver.get(URL)
query = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
query.send_keys(search_word, Keys.ENTER)
