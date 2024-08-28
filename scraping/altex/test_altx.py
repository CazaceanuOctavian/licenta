import re
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import NavigableString
from bs4 import BeautifulSoup

def no_nav_strings(iterable):
    return list(filter(lambda x: type(x) != NavigableString, iterable))

options = Options()
options.binary_location = '/etc/firefox'
options.accept_insecure_certs = True


profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox(options=options)

driver.get('https://altex.ro/tablete/cpl/')

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
html_content = soup.prettify()
with open('htmldump.txt', 'w') as file:
    file.write(html_content)

li_items = soup.find_all(class_=re.compile("products-item", re.IGNORECASE))


def format_data(item):
    try:
        name = item.a.next_sibling.text
        isInStoc = item.a.find_next_sibling(class_=re.compile('text-13px', re.IGNORECASE))
        raw_rating = item.a.find_next_sibling(class_=re.compile('truncate my-1', re.IGNORECASE))
        raw_price = item.a.find_next_sibling(class_=re.compile('mb-0', re.IGNORECASE))

        if raw_rating == None:
            raw_rating = 'NULL'
        print(name + '----' + isInStoc.text + '-----' + raw_rating.text + '-----' + raw_price.text)

        return {
            'name' : name,
            'raw_price' : raw_price.text,
            'raw_rating' : raw_rating.text,
            'is_in_stoc' : isInStoc.text
        }
    
    except:
        print('EXCEPTION====='+str(name)+str(isInStoc)+str(raw_rating)+str(raw_price)+'=====EXCEPTION')
        driver.quit()
    

with open('test-dump.txt', 'w') as testdump:
    for item in li_items:
        item = no_nav_strings(item.descendants)

        formatted_dict = format_data(item[0])
        json_dump = json.dumps(formatted_dict)
        testdump.write(json_dump+'\n')
        # json_dump = json.dumps(product_dict)
        # testdump.write(json_dump + '\n')
        # #name
        # testdump.write(item[0].a.next_sibling.text + '-----')
        # #isInStoc
        # testdump.write(item[0].a.next_sibling.next_sibling.next_sibling.text + '-----')
        # #rating
        # testdump.write(item[0].a.next_sibling.next_sibling.next_sibling.next_sibling.text + '-----')
        # #pret
        # testdump.write(item[0].a.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text + '\n')

driver.quit()


