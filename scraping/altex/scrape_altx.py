import re
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup

options = Options()
options.binary_location = '/etc/firefox'

driver = webdriver.Firefox(options=options)

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

def scrape(path):
    target_url = "https://altex.ro" + path
    driver.get(target_url)

    
    pagina_existenta = True
    current_page = 1
    while(pagina_existenta):
        current_page +=1
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        html_content = soup.prettify()
        with open('htmldump.txt', 'w') as file:
            file.write(html_content)

        test = soup.find(class_=re.compile('font-normal text-base', re.IGNORECASE))
        if test is not None:
            break

        li_items = soup.find_all(class_=re.compile("products-item", re.IGNORECASE))

        with open('Altx_scrape.txt', 'a') as scrapefile:
            for element in li_items:
                formatted_dict = format_data(element)
                json_dump = json.dumps(formatted_dict)
                scrapefile.write(json_dump+'\n')

        new_path = target_url + 'filtru/p/' + str(current_page) + '/'
        driver.delete_all_cookies()
        driver.get(new_path)
        
def main():
    with open('Altx_Tree.txt', 'r') as file:
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