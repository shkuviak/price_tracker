import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import json

parser = argparse.ArgumentParser(description='Scrape Nike Website')
parser.add_argument('-u', '--url',  help='Nike product URL', dest='url',
      metavar='url', required=True)


args = parser.parse_args()

def crawler(url):
    # urlpage = 'https://www.nike.com/fr/t/chaussure-air-force-1-07-pour-pXTXQ8/CT2302-002' 
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path = './geckodriver.exe')
    driver.get(url)

    res_dict = {
        "type": 'clothes',
        "name":"",
        "price": -1,
        "photo_alt": "",
        "photo_src": "",
        "sizes": {} 
    }
    product_name = driver.find_elements(by=By.XPATH, value='//h1[@id="pdp_product_title"]')[1]
    # print(product_name.text)

    price = driver.find_elements(by=By.XPATH, value='//div[@data-test="product-price"]')[1]
    # print(price.text)

    photo = driver.find_elements(by=By.XPATH, value='//div[@class="colorway-images-wrapper"]/fieldset/div/div/input[@checked=""]/../label/img')[0]
    # print(photo.get_attribute("alt"))
    # print(photo.get_attribute("src"))

    res_dict["name"] = product_name.text
    res_dict["price"] = price.text
    res_dict["photo_alt"] = photo.get_attribute("alt")
    res_dict["photo_src"] = photo.get_attribute("src")

    results = driver.find_elements(by=By.XPATH, value='//form[@id="buyTools"]/div[1]/fieldset/div/div')

    for size_box in results:
        size = size_box.find_elements(by=By.XPATH, value='label')[0].text
        available =  False if len(size_box.find_elements(by=By.XPATH, value='input[@disabled=""]')) > 0 else True
        # print(size, available)
        res_dict["sizes"][size] = available

    driver.quit()

    return res_dict

if __name__=='__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Scrape Nike Website')
    parser.add_argument('-u', '--url',  help='Nike product URL', dest='url',
        metavar='url', required=True)


    args = parser.parse_args()

    result = crawler(args.url)
    print(json.dumps(result))
    
