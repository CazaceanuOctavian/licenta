import re
import os
import csv
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import NavigableString
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
#options.add_argument('--headless')
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
        #price = float(item.find_next(class_='real_price').text.strip().replace(',','.').split(' ')[0])
        price = float(item.find_next(class_='real_price').text.split(' ')[0].replace('.','').replace(',','.'))

        try:
            #evomag are hidden un 'fa cadou' in care mai e o imagine care este scraped din greseala
            #imaginea e ascunsa in item, asa ca item.find_next o ia pe ea in loc de imaginea cautata
            #Solutie --> move forward to the next sibling si apoi apeleaza find_next()
            imageUrl = item.next_sibling.find_next(loading = 'lazy') 
            if imageUrl['alt']=='Offer':
                imageUrl = imageUrl.find_next(loading = 'lazy')['src']
            else :
                imageUrl =imageUrl['src']
        except Exception as e:
            imageUrl = 'err'

        driver.delete_all_cookies()
        driver.get(itemUrl)

        WebDriverWait(driver, 2).until( EC.presence_of_all_elements_located )

        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        product_code = other_soup.find(class_='product_codes').span.text.strip()
        match = re.search(r'\[ (.*?) \]', product_code)
        if match:
            product_code = match.group(1)
        
        product_code = product_code.replace('/','+rep+')

        #=====scraping image=====
        if imageUrl != 'err':
            try:
                img_data = requests.get(imageUrl).content
                img_name = product_code + '.jpeg'
                #
                filepath = os.path.join('/home/tavi/Desktop/licenta/frontend/public/images', img_name) 
                with open(filepath, 'wb') as file:
                    file.write(img_data)
            except Exception as e:
                print('could not get image, so sad...')
                with open('errLog.txt', 'a') as logs:
                    logs.write('ERR FOR PRODUCT: ' + name)
                    logs.write('ERR: ' + str({e}) + '\n')
                filepath = 'err'
            #=====scraping image=====

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'evomag',
            'img_path' : filepath 
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION====='+str(name)+str(isInStoc)+'=====EXCEPTION')
        with open('errLog.txt', 'a') as logs:
            logs.write('ERR FOR PRODUCT: ' + name)
            logs.write('ERR: ' + str({e}) + '\n')
    

def scrape(path):
    target_url = 'https://www.evomag.ro' + path
    #target_url = path
    driver.get(target_url)

    #wait for images to lazly load
    element = WebDriverWait(driver, 2)

    pagina_existenta = True
    current_page = 1
    while(pagina_existenta):
        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        with open('dump.txt', 'w') as dump:
            dump.write(page_source)
        
        li_items = soup.find_all(class_="nice_product_item")
        category = soup.find(class_='breadcrumbs').text.strip().split('»')[-1].strip()

        if li_items == []:
            break

        next_page_button = soup.find(attrs= {'class' : 'next hidden'})
        if next_page_button is not None:
            break

        next_page_button = soup.find(attrs= {'class' : 'next'})
        if next_page_button is None:
            break

        with open('evomag_scrape_shitted.csv', 'a') as scrapefile:
                writer = csv.writer(scrapefile)
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category']=category
 
                        writer.writerow(formatted_dict.values())
                    except Exception as e:
                        print(str({e}))
                        with open('errLog.txt', 'a') as logs:
                            logs.write('ON PATH:' + path +  '\n' + 'PAGE:' + str(current_page) + '\n')
                        continue
        new_path = target_url + 'filtru/pagina:' + str(current_page) 
        driver.delete_all_cookies()
        driver.get(new_path)
                
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

#scrape('/portabile-laptopuri-notebook/filtru/pagina:2')

main()
driver.quit()