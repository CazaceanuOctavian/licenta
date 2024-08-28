import re
import json
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import NavigableString
from bs4 import BeautifulSoup

options = Options()

options.binary_location = '/etc/firefox'

driver = webdriver.Firefox(options=options)

def no_nav_strings(iterable):
    return list(filter(lambda x: type(x) != NavigableString, iterable))

def format_data(item):
    try:
        items = list(item.find_next_siblings())
        middle = items[0]
        children_of_middle = list(middle.children)
        name = children_of_middle[3].text

        rating_container = item.find_next(class_='rating_container')
        product_stars = -1
        if rating_container is not None:
            product_stars = rating_container.children 

            cnt = 0
            for star in product_stars:
                if star['class'] == ['rating_on']:
                    cnt+=1
            product_stars = cnt

        price = item.find_next(class_='pb-price').text
        isInStoc = item.find_next(class_=re.compile('product_box_availability', re.IGNORECASE)).text.strip()

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : product_stars,
            'is_in_stoc' : isInStoc
        }
    
    #name, raw_price, raw_rating, is_in_stoc
    except:
        print('EXCEPTION====='+str(name)+'=====EXCEPTION')

def scrape(path):
    target_url = path
    driver.get(target_url)

    pagina_existenta = True
    current_page = 0
    while(pagina_existenta):
        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        test = soup.find(class_='page_heading')
        if test.text == 'Pagina inexistenta':
            break

        html_content = soup.prettify()
        with open('htmldump.txt', 'w') as file:
            file.write(html_content)
        
        li_items = soup.find_all(class_="product_box")

        with open('pc_garage_scrape.txt', 'a') as scrapefile:
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        json_dump = json.dumps(formatted_dict)
                        scrapefile.write(json_dump+'\n')
                    except:
                        break
        new_path = path + 'pagina' + str(current_page) + '/'
        driver.delete_all_cookies()
        driver.get(new_path)



#validare-access
                
def main():
    print(os.getcwd())
    with open('pc_gar_tree.txt', 'r') as file:
        for path in file:
            driver.delete_all_cookies()
            path = path.strip()
            if path is None:
                continue
            try:
                scrape(path=path)
            except:
                driver.delete_all_cookies()
                continue

main()
driver.quit()