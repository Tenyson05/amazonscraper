import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = "https://www.amazon.com/"

driver = webdriver.Firefox()
driver.get(URL)