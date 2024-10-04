import re
import os
import csv
import requests
import datetime
import configparser
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import NavigableString
from bs4 import BeautifulSoup

options = Options()
#options.add_argument('--headless')
options.binary_location = '/nix/store/z5lcsw013vbkgwxw6n7kx9lgbadqf7vy-firefox-130.0.1/bin/firefox'
options.page_load_strategy = 'normal'
driver = webdriver.Firefox(options=options)
try:
    driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
    driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/jid1-MnnxcxisBPnSXQ@jetpack.xpi')
    driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/langpack-en-US@firefox.mozilla.org.xpi')
    driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/uBlock0@raymondhill.net.xpi')
except Exception as e:
    print('WARNING: Could not install some add-ons...')

currentDate = datetime.datetime.now().strftime('%Y_%m_%d')

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

latest_path = None


def no_nav_strings(iterable):
    return list(filter(lambda x: type(x) != NavigableString, iterable))

def format_data(item):
    try:
        manufacturer = item.find_next(class_='manufacturer pull-left').text.strip().lower()
        name = item.find_next(class_='name').text.strip()
        isInStoc = item.find_next(class_=re.compile('availability margin-bottom-xs', re.IGNORECASE)).text.strip()
        test = isInStoc[:2]
        if isInStoc[:2] == 'in':
            isInStoc = 1
        else:
            isInStoc = 0

        # try:
        #     price = float(item.find_next(class_='price margin-bottom-xs clearfix col-xs-6 grid-full').text.strip().replace(',','.').split(' ')[0])
        # except Exception as e:
        #     #TODO -->fix bug where this gets value of 2.7 instead of 2799 
        #     price = float(item.find_next(class_='price margin-bottom-xs clearfix col-xs-6 grid-full').text.strip().split('\n')[-1].split(' ')[0].split(',')[0])

        

        itemUrl = item.find_parent().findPreviousSibling().a['href']
        #TODO -->fix bug when the first image off of every big page gets skipped 
        try:
            imageUrl = item.find_previous('img')['data-src']
            #imageUrl = item.find_parent().findPreviousSibling().find_next('img')['data-src']
        except Exception as e:
            imageUrl = 'err'

        driver.delete_all_cookies()
        driver.get(itemUrl)
        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        #WebDriverWait(driver, 2).until( EC.presence_of_all_elements_located )

        product_code = other_soup.find(class_='model').text.strip()
        product_code = product_code.replace('/','+rep+')

        raw_price = other_soup.find(id='price-value').text
        if '.' in raw_price:
            raw_price = raw_price.replace('.','')
        price = float(raw_price.replace('"','').strip().split(' ')[0].replace(',', '.'))

        #=====scraping image=====   
        if imageUrl != 'err':
            try:
                img_data = requests.get(imageUrl).content
                img_name = product_code + '.jpeg'
                #
                filepath = os.path.join(config['Paths']['image_output'], img_name) 
                with open(filepath, 'wb') as file:
                    file.write(img_data)
            except Exception as e:
                with open(config['Paths']['vexio_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                    logs.write('ERR FOR IMAGE SCRAPING: ' + name)
                    logs.write('ERR: ' + str({e}) + '\n')
                img_name = 'not_found.jpeg'
        #=====scraping image=====

        print('vexio -- ' + name)

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'vexio',
            'img_path' : '/images/' + img_name,
            'manufacturer' : manufacturer
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION VEXIO====='+str(name)+str(isInStoc)+'=====EXCEPTION VEXIO')
        with open(config['Paths']['vexio_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
            logs.write('ERR IN FORMAT_DATA FOR PRODUCT: ' + name)
            logs.write('ERR: ' + str({e}) + '\n')

    print()

def scrape(path : str):
    target_url = path

    global latest_path
    latest_path = path

    if path.rfind("pagina") == -1:
        current_page = 1
    else:
        current_page = int(path.split('/')[-2][-1])
        path = path.split('pagina' + str(current_page) + '/')[0]


    driver.get(target_url)

    pagina_existenta = True
    while(pagina_existenta):

        current_page+=1
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        li_items = soup.find_all(class_="grid-full col-xs-8 col-sm-4 col-md-4")
        category = soup.find(class_='breadcrumb').text.strip().split('\xa0')[-1]
        next_page_button = soup.find(class_ = 'pagination-next')

        with open(config['Paths']['vexio_output'] + 'vexio_' + str(currentDate) + '.csv', 'a', newline='') as scrapefile:
                writer = csv.writer(scrapefile)
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category'] = category

                        writer.writerow(formatted_dict.values())
                    except Exception as e:
                        print(str({e}))
                        with open(config['Paths']['vexio_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                            logs.write('ON PATH:' + path +  '\n' + 'PAGE:' + str(current_page) + '\n')
                        continue

        if (next_page_button == None):
            break

        new_path = path + 'pagina' + str(current_page) + '/'
        latest_path = new_path

        driver.delete_all_cookies()
        driver.get(new_path)
           
def main():
    try:
        print(os.getcwd())  
        origin = os.path.join(config['Paths']['vexio_output'], 'dying_gasp_' + str(currentDate) + '.txt')
        pathCount=0

        if (os.path.exists(origin)):
            print('DYING GASP DETECTED -- DEFAULTING TO ' + str(origin) + ' -- SCRAPING FROM LAST KNOWN PATH')
        else:
            print('NO DYING GASP -- DEFAULTING TO vexio_tree.txt')
            origin = config['Paths']['vexio_output'] + 'vexio_tree.txt' 

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
                    with open(config['Paths']['vexio_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                        logs.write('ERR MAIN: ' + str({e}))
                    driver.delete_all_cookies()
                    continue
    finally:
        #write the remaining lines in dying_gasp from current line to EOF
        print('PANIC!')
        with open(config['Paths']['vexio_output'] + 'dying_gasp_' + str(currentDate) + '_tmp.txt', 'w') as gasp:
            gasp.write(latest_path + '\n')

            with open(origin, 'r') as origin_file:
                for _ in range(pathCount):
                    origin_file.readline()

                line = origin_file.readline()
                gasp.write(line)
                while(line):
                    line = origin_file.readline()
                    gasp.write(line)
        os.rename(config['Paths']['vexio_output'] +  'dying_gasp_' + str(currentDate) + '_tmp.txt', config['Paths']['vexio_output'] + 'dying_gasp_' + str(currentDate) + '.txt')
        driver.quit()

main()
driver.quit()