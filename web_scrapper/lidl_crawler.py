import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import json



def crawler(url):
    # urlpage = 'https://www.nike.com/fr/t/chaussure-air-force-1-07-pour-pXTXQ8/CT2302-002' 
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path = './geckodriver.exe')
    driver.get(url)

    res_dict = {
        "type": 'object',
        "name":"",
        "price": -1,
        "photo_src": "",
        "available": False 
    }
    product_name = driver.find_elements(by=By.XPATH, value='//h1[@class="keyfacts__title"]')[0]
    # print(product_name.text)

    price = driver.find_elements(by=By.XPATH, value='//div[@class="m-price__price"]')[0]
    # print(price.text)

    photo = driver.find_elements(by=By.XPATH, value='//img[@class="gallery-image__img"]')[0]
    # print(photo.get_attribute("alt"))
    # print(photo.get_attribute("src"))

    res_dict["name"] = product_name.text
    res_dict["price"] = price.text
    res_dict["photo_src"] = photo.get_attribute("src")

    add_to_cart = driver.find_element(by=By.XPATH, value='//button[@id="addToCart"]')
    available = False if add_to_cart.get_attribute("disabled") else True

    res_dict["available"] = available

    driver.quit()

    return res_dict

if __name__=='__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Scrape Lidl.be Website')
    parser.add_argument('-u', '--url',  help='Lidl product URL', dest='url',
        metavar='url', required=True)

    args = parser.parse_args()

    result = crawler(args.url)
    print(json.dumps(result))