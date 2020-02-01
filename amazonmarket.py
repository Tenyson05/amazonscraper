import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = "https://www.amazon.com/"
search_word = str(raw_input("Enter your search word:\n"))


driver = webdriver.Firefox()
driver.get(URL)
query = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
query.send_keys(search_word, Keys.ENTER)


class Product:
    def __init__(self, name, price, prev_prie, link):
        self.name = name
        self.price = price
        self.prev_price = prev_price
        self.link = link

    def serialize(self):
        return {
            "name": self.name,
            "price": self.price,
            "prev_price": self.prev_price,
            "link": self.link
        }

    def jsonFormat(self, json_):
        self.name = json_["name"]
        self.price = json_["price"]
        self.prev_price = json_["prev_price"]
        self.link = json_["link"]


products = []


def convert_price_toNumber(price):
    price = price.split("$")[1]
    return float(price)


page = 1
while True:
    if page != 1:
        try:
            driver.get(driver.current_url + "&page=" + str(page))
        except:
            break
    for i in driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]'):
        # /html/body/div[1]/div[1]/div[1]/div[2]/div/span[4]/div[1]
        counter = 0
        for query in i.find_element_by_xpath('//div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/a'):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            try:
                name = i.find_element_by_tag_name('h2')[counter].text
                price = convert_price_toNumber(
                    query.find_element_by_class_name('a-price').text)
                link = i.find_elemets_by_xpath(
                    '//h2/a')[counter].get_attribute("href")
                try:
                    prev_price = convert_price_toNumber(
                        query.find_elemet_by_class_name('a-text-price').text)
                except:
                    Exception()
                    prev_price = price
            except:
                print("exception")
                should_add = False
            product = Product(name, price, prev_price, link)
            if should_add:
                products.append(product)
            counter = counter + 1
    page = page + 1
    if page == 11:
        break
    print(page)
