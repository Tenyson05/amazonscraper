import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = "https://www.amazon.com/s?k="


options = webdriver.FirefoxOptions()
driver = webdriver.Firefox()

search_word = str(input("Enter your search word:\n"))

driver.get(URL)
query = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
query.send_keys(search_word, Keys.ENTER)
time.sleep(3)



class Product:
    def __init__(self, name, price, prev_price, link):
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
    try:
        price = price.split("\n")[0] + "." + price.split("\n")[1]
    except:
        Exception()
    try:
        price = price.split(",")[0] + price.split(",")[1]
    except:
        Exception()
    return float(price)


page = 1
while True:
    if page != 0:
        try:
            driver.get(driver.current_url+ "&page=" + str(page))
        except:
            break
    for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]'):
        # /html/body/div[1]/div[1]/div[1]/div[2]/div/span[4]/div[1]
        counter = 0
        for query in i.find_elements_by_xpath('//div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/a'):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            try:
                name = i.find_elements_by_tag_name('h2')[counter].text
                price = convert_price_toNumber(query.find_element_by_class_name('a-price').text)
                link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")
                try:
                    prev_price = convert_price_toNumber(query.find_element_by_class_name('a-text-price').text)
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
    page = page +1
    if page == 11:
        break
    print(str(page) + " " + str(driver.current_url))

biggest_discount = 0.0
lowest_price = 0.0
cheapest_product = Product("", "", "", "")
best_deal_product = Product("", "", "", "")
search_word = search_word.split(" ")

run = 0

for product in products:
    not_right = False
    for word in search_word:
        if word.lower() not in product.name.lower():
            not_right = True
    if not not_right:
        if run == 0:
            lowest_price = product.price
            cheapest_product = product
            run = 1
        elif product.price < lowest_price:
            lowest_price = product.price
            cheapest_product = product
        discount = product.prev_price - product.price
        if discount > biggest_discount:
            biggest_discount = discount
            best_deal_product = product

with open('products.json', 'w') as json_file:
    data = {}
    data["Products"] = []
    for prod in products:
        data["Products"].append(prod.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)

print(json.dumps(cheapest_product.serialize(), indent=4, sort_keys=True))
print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))


driver = webdriver.Firefox()
driver.get(best_deal_product.link)
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')