import re
import os
import csv
import requests
import datetime

from bs4 import NavigableString
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
#options.add_argument('--headless')
options.binary_location = '/etc/firefox'
driver = webdriver.Firefox(options=options)

currentDate = datetime.datetime.now().strftime('%Y_%m_%d')

latest_path = None

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
                with open('output/errLog-' + str(currentDate) + '.txt', 'a') as logs:
                    logs.write('ERR FOR IMAGE SCRAPING: ' + name)
                    logs.write('ERR: ' + str({e}) + '\n')
                img_name = 'not_found.jpeg'
            #=====scraping image=====

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'evomag',
            'img_path' : '/images/' + img_name
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION====='+str(name)+str(isInStoc)+'=====EXCEPTION')
        with open('output/errLog-' + str(currentDate) + '.txt', 'a') as logs:
            logs.write('ERR IN FORMAT_DATA FOR PRODUCT: ' + name)
            logs.write('ERR: ' + str({e}) + '\n')
    

def scrape(path : str):

    if path.rfind("https") == -1:
        target_url = 'https://www.evomag.ro' + path
        current_page = 1
    else:
        target_url = path
        current_page = int(path.split(":")[-1].split('/')[0])

    global latest_path
    latest_path = path

    driver.get(target_url)

    #wait for images to lazly load
    element = WebDriverWait(driver, 2)

    pagina_existenta = True
    while(pagina_existenta):
        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # with open('dump.txt', 'w') as dump:
        #     dump.write(page_source)
        
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

        with open('output/evomag_' + str(currentDate) + '.csv', 'a', newline='') as scrapefile:
                writer = csv.writer(scrapefile)
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category']=category
 
                        writer.writerow(formatted_dict.values())
                        
                    except Exception as e:
                        print(str({e}))
                        with open('output/errLog-' + str(currentDate) + '.txt', 'a') as logs:
                            logs.write('ON PATH:' + path +  '\n' + 'PAGE:' + str(current_page) + '\n')
                        continue
                    
        
        new_path = target_url + 'filtru/pagina:' + str(current_page) 

        latest_path = new_path

        driver.delete_all_cookies()
        driver.get(new_path)
                
def main():
    try:
        origin = os.path.join('output', 'dying_gasp_' + str(currentDate) + '.txt')
        pathCount = 0
        global latest_path

        if (os.path.exists(origin)):
            print('DYING GASP DETECTED -- DEFAULTING TO ' + str(origin) + ' -- SCRAPING FROM LAST KNOW PATH')
        else:
            print('NO DYING GASP -- DEFAULTING TO evomag_tree.txt')
            origin = 'evomag_tree.txt' 

        with open(origin, 'r') as origin_file:
            for path in origin_file:
                pathCount+=1

                driver.delete_all_cookies()
                path = path.strip()
                
                if path is None:
                    continue
                try:
                    scrape(path=path)
                except Exception as e:
                    print(str({e}))
                    with open('output/errLog-' + str(currentDate) + '.txt', 'a') as logs:
                        logs.write('ERR MAIN: ' + str({e}))
                    driver.delete_all_cookies()
                    continue
    except KeyboardInterrupt as end:
        #write the remaining lines in dying_gasp from current line to EOF
        print('PANIC!')
        with open('output/dying_gasp_' + str(currentDate) + '_tmp.txt', 'w') as gasp:
            gasp.write(latest_path)
            
            with open(origin, 'r') as origin_file:
                for _ in range(pathCount):
                    origin_file.readline()

                line = origin_file.readline()
                gasp.write(line)
                while(line):
                    line = origin_file.readline()
                    gasp.write(line)
        os.rename('output/dying_gasp_' + str(currentDate) + '_tmp.txt', 'output/dying_gasp_' + str(currentDate) + '.txt')
        
main()
driver.quit()