import re
import json
import os
import csv

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import NavigableString
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
options.binary_location = '/etc/firefox'

driver = webdriver.Firefox(options=options)

def no_nav_strings(iterable):
    return list(filter(lambda x: type(x) != NavigableString, iterable))

def format_data(item):
    try:
        name = item.find_next(class_='name').text.strip()
        isInStoc = item.find_next(class_=re.compile('availability margin-bottom-xs', re.IGNORECASE)).text.strip()
        test = isInStoc[:2]
        if isInStoc[:2] == 'in':
            isInStoc = 1
        else:
            isInStoc = 0
        print(name)
        price = float(item.find_next(class_='price margin-bottom-xs clearfix col-xs-6 grid-full').text.strip().replace(',','.').split(' ')[0])
        itemUrl = item.find_parent().findPreviousSibling().a['href']

        driver.delete_all_cookies()
        driver.get(itemUrl)

        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        product_code = other_soup.find(class_='model').text.strip()

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'vexio' 
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION====='+str(name)+str(isInStoc)+'=====EXCEPTION')


    print()

def scrape(path):
    target_url = path
    driver.get(target_url)

    pagina_existenta = True
    current_page = 1

    while(pagina_existenta):
        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        last_url = driver.current_url

        html_content = soup.prettify()
        with open('htmldump.txt', 'w') as file:
            file.write(html_content)
        
        li_items = soup.find_all(class_="grid-full col-xs-8 col-sm-4 col-md-4")
        category = soup.find(class_='breadcrumb').text.strip().split('\xa0')[-1]

        with open('vexio_scrape_new.csv', 'a', newline='') as scrapefile:
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category'] = category

                        writer = csv.writer(scrapefile)
                        writer.writerow(formatted_dict.values())
                    except Exception as e:
                        print(str({e}))
                        break
      
        new_path = path + 'pagina' + str(current_page) + '/'
        driver.delete_all_cookies()
        driver.get(new_path)

        url_test = driver.current_url

        if last_url == url_test:
            break
           
def main():
    print(os.getcwd())  
    with open('vexio_tree_new.txt', 'r') as file:
        for path in file:
            driver.delete_all_cookies()
            path = path.strip()
            if path is None:
                continue
            try:

                scrape(path=path)
            except Exception as e:
                print(str({e}))
                driver.delete_all_cookies()
                continue

main()
driver.quit()