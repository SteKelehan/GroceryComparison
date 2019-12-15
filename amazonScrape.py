# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import sys
# import configparser



# URLStart = 'https://www.amazon.co.uk/s?k='
# URLEnd = '&i=amazonfresh&ref=nb_sb_noss_1'
# config = configparser.ConfigParser()
# config.read('config.ini')
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# session = requests.Session()
# session.headers = config['Amazon']['header2']
# # URL = config['Amazon']['URLSignIn']
# resp = session.get(config['Amazon']['URLSignIn'])
# html = resp.text

# soup = BeautifulSoup(html , 'lxml')
# data = {}
# form = soup.find('form', {'name': 'signIn'})
# for field in form.find_all('input'):
#     try:
#         data[field['name']] = field['value']
    
#     except:
#         pass

# data[u'email'] = config['Amazon']['User'] 
# data[u'password'] = config['Amazon']['Password']

# post_resp = session.post(config['Amazon']['URLSignIn'], data = data)

# post_soup = BeautifulSoup(post_resp.content , 'lxml')

# if post_soup.find_all('title')[0].text == 'Your Account':
#     print('Login Successfull')
# else:
#     print('Login Failed')



# def get_product_details(product):
#     cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
#     product = product.replace(' ', '+')
#     url = URLStart + product + URLEnd
#     data = requests.get(url, headers=headers, cookies=cookies)
#     content = data.content
#     soup = BeautifulSoup(content)
#     print(soup)
#     return data


# get_product_details('oat milk')



import requests 
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from product import Product

URL = "http://www.amazon.co.uk/"
  
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/Ste/Downloads/chromedriver", chrome_options=options)

search_term = str(input("What are you looking for?\n:"))

driver.get(URL)
element = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
element.send_keys(search_term)
element.send_keys(Keys.ENTER)

products = []


def convert_price_toNumber(price):

    price = price.split("£")[1]
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
    if page != 1:
        try:
            driver.get(driver.current_url + "&page=" + str(page))
        except:
            break
    for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]'):

        counter = 0
        for element in i.find_elements_by_xpath('//div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/a'):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            try:
                name = i.find_elements_by_tag_name('h2')[counter].text
                price = convert_price_toNumber(element.find_element_by_class_name('a-price').text)
                link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")
                try:
                    prev_price = convert_price_toNumber(element.find_element_by_class_name('a-text-price').text)
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
    if page == 3:
        break
    print(page)

print("done")
