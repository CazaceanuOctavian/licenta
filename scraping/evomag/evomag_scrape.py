import re
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
        name = item.find_next(class_='npi_name').text.strip()
        itemUrl = 'https://www.evomag.ro' + item.find_next(class_='npi_name').h2.a['href']
        isInStoc = item.find_next(class_=re.compile('stock_', re.IGNORECASE)).text.strip()
        if isInStoc[:2] == 'In':
            isInStoc = 1
        else:
            isInStoc = 0
        print(name)
        #price = float(item.find_next(class_='real_price').text.strip().replace(',','.').split(' ')[0])
        price = float(item.find_next(class_='real_price').text.split(' ')[0].replace('.','').replace(',','.'))


        driver.delete_all_cookies()
        driver.get(itemUrl)

        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        product_code = other_soup.find(class_='product_codes').span.text.strip()
        match = re.search(r'\[ (.*?) \]', product_code)
        if match:
            product_code = match.group(1)

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'evomag'
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION====='+str(name)+str(isInStoc)+'=====EXCEPTION')


    print()

def scrape(path):
    target_url = 'https://www.evomag.ro' + path
    #target_url = path
    driver.get(target_url)

    pagina_existenta = True
    current_page = 1
    while(pagina_existenta):
        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # html_content = soup.prettify()
        # with open('htmldump.txt', 'w') as file:
        #     file.write(html_content)
        
        li_items = soup.find_all(class_="nice_product_item")
        category = soup.find(class_='breadcrumbs').text.strip().split('»')[-1].strip()

        if li_items == []:
            break

        with open('evomag_scrape_new.csv', 'a') as scrapefile:
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category']=category
 
                        writer = csv.writer(scrapefile)
                        writer.writerow(formatted_dict.values())
                    except Exception as e:
                        print(str({e}))
                        break

        next_page_button = soup.find(attrs= {'class' : 'next hidden'})
        if next_page_button is not None:
            break

        next_page_button = soup.find(attrs= {'class' : 'next'})
        if next_page_button is None:
            break

        new_path = target_url + 'filtru/pagina:' + str(current_page) 
        driver.delete_all_cookies()
        driver.get(new_path)


#validare-access
                
def main():
    print(os.getcwd())
    with open('evomag_tree.txt', 'r') as file:
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
#debug
#scrape('https://www.evomag.ro/telefoane-tablete-accesorii-tablete-epaper-accesorii-tablete-epaper/filtru/pagina:89')

#end debug


driver.quit()