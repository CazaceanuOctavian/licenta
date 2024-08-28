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

driver.get('https://www.pcgarage.ro/ultrabook/')

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
html_content = soup.prettify()
with open('htmldump.txt', 'w') as file:
    file.write(html_content)

li_items = soup.find_all(class_='product_box')


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

        # for child_of_upper in children_of_upper:
        #     if child_of_upper != ' ':
        #         print(child_of_upper.text)
        # return {
        #     'name' : name,
        #     'raw_price' : raw_price.text,
        #     'raw_rating' : raw_rating.text,
        #     'is_in_stoc' : isInStoc.text
        # }
    
    except:
        print('EXCEPTION====='+str(name)+'=====EXCEPTION')
        driver.quit()
    

with open('test-dump.txt', 'w') as testdump:
    for item in li_items:
        item = no_nav_strings(item.descendants)

        formatted_dict = format_data(item[0])
        json_dump = json.dumps(formatted_dict)
        testdump.write(json_dump+'\n')


driver.quit()


