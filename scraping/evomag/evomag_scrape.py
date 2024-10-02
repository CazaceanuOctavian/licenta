import re
import os
import csv
import requests
import datetime
import configparser
import time

from bs4 import NavigableString
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# def install_addons():
#     try:
#         driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
#         driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/jid1-MnnxcxisBPnSXQ@jetpack.xpi')
#         driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/langpack-en-US@firefox.mozilla.org.xpi')
#         driver.install_addon('/home/tav/snap/firefox/common/.mozilla/firefox/53alnjep.default/extensions/uBlock0@raymondhill.net.xpi')
#     except Exception as e:
#         print('WARNING: Could not install some add-ons...')


def create_driver():
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.set_preference("browser.privatebrowsing.autostart", True)

    options.binary_location = '/nix/store/z5lcsw013vbkgwxw6n7kx9lgbadqf7vy-firefox-130.0.1/bin/firefox'
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=options)
    return driver
    # install_addons()
# driver.execute_script("window.setTimeout(() => window.close(), 1000);")

#install_addons()

currentDate = datetime.datetime.now().strftime('%Y_%m_%d')

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

latest_path = None

def no_nav_strings(iterable):
    return list(filter(lambda x: type(x) != NavigableString, iterable))

def format_data(item,driver):
    try:
        # driver.execute_script("Services.clearData.deleteData(Services.clearData.CLEAR_ALL);")

        #time.sleep(5)
        # all_objects = muppy.get_objects()
        # my_sum = summary.summarize(all_objects)
        # summary.print_(my_sum)

        name = item.find_next(class_='npi_name').text.strip()
        itemUrl = 'https://www.evomag.ro' + item.find_next(class_='npi_name').h2.a['href']
        isInStoc = item.find_next(class_=re.compile('stock_', re.IGNORECASE)).text.strip()
        if isInStoc[:2] == 'In':
            isInStoc = 1
        else:
            isInStoc = 0
        #price = float(item.find_next(class_='real_price').text.strip().replace(',','.').split(' ')[0])
        #price = float(item.find_next(class_='real_price').text.split(' ')[0].replace('.','').replace(',','.'))
        price = item.find_next(class_='real_price').text.split(' ')[0].replace('.','')
        price = float(price[:-2] + '.' + price[-2:]) 

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

        # Wait for an element with a specific ID to appear (e.g., 'myElement')
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_codes"))
        )

        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        em_elems = other_soup.find_all('em')
        manufacturer = em_elems[-2].text.strip().lower()

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
                filepath = os.path.join('/home/tav/Desktop/licenta/frontend/public/images', img_name) 
                with open(filepath, 'wb') as file:
                    file.write(img_data)
            except Exception as e:
                with open(config['Paths']['evomag_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                    logs.write('ERR FOR IMAGE SCRAPING: ' + name)
                    logs.write('ERR: ' + str({e}) + '\n')
                img_name = 'not_found.jpeg'
            #=====scraping image=====

        print('evomag -- ' + name)

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'evomag',
            'img_path' : '/images/' + img_name,
            'manufacturer': manufacturer
            }
    
    except Exception as e:
        print(str({e}))
        print('EXCEPTION EVOMAG====='+str(name)+str(isInStoc)+'=====EXCEPTION EVOMAG')
        with open(config['Paths']['evomag_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
            logs.write('ERR IN FORMAT_DATA FOR PRODUCT: ' + name)
            logs.write('ERR: ' + str({e}) + '\n')
    

def scrape(path : str):
    driver = None
    if driver is None:
        driver = create_driver()
    
    if path.rfind("https") == -1:
        target_url = 'https://www.evomag.ro' + path
        current_page = 1
    else:
        #TODO --> this may be stupid 
        target_url = path.split('https://www.evomag.ro')[-1]
        current_page = int(path.split(":")[-1].split('/')[0])
        target_url = path.split('filtru/pagina:' + str(current_page))[0]

    global latest_path
    latest_path = path 

    driver.get(target_url + 'filtru/pagina:' + str(current_page))

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

        with open(config['Paths']['evomag_output'] + 'evomag_' + str(currentDate) + '.csv', 'a', newline='') as scrapefile:
                writer = csv.writer(scrapefile)
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0], driver)
                        formatted_dict['category']=category
 
                        writer.writerow(formatted_dict.values())
                        
                    except Exception as e:
                        print(str({e}))
                        with open(config['Paths']['evomag_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                            logs.write('ON PATH:' + path +  '\n' + 'PAGE:' + str(current_page) + '\n')
                        continue

        next_page_button = soup.find(attrs= {'class' : 'next hidden'})
        if next_page_button is not None:
            break

        next_page_button = soup.find(attrs= {'class' : 'next'})
        if next_page_button is None:
            break
                    
        new_path = target_url + 'filtru/pagina:' + str(current_page) 

        latest_path = new_path

        #print('LEAKS-----'+ str(leaks) + 'LEAKS-----')

        driver.delete_all_cookies()
        driver.quit()
        driver = create_driver()
        driver.get(new_path)

    driver.quit()


def main():
    try:
        origin = os.path.join(config['Paths']['evomag_output'], 'dying_gasp_' + str(currentDate) + '.txt')
        pathCount = 0
        global latest_path

        if (os.path.exists(origin)):
            print('DYING GASP DETECTED -- DEFAULTING TO ' + str(origin) + ' -- SCRAPING FROM LAST KNOW PATH')
        else:
            print('NO DYING GASP -- DEFAULTING TO evomag_tree.txt')
            origin = config['Paths']['evomag_output'] + 'evomag_tree.txt' 

        with open(origin, 'r') as origin_file:
            for path in origin_file:
                pathCount+=1
                path = path.strip()
                
                if path is None:
                    continue
                try:
                   scrape(path=path)
                   
                except Exception as e:
                    print(str({e}))
                    with open(config['Paths']['evomag_output'] + 'errLog-' + str(currentDate) + '.txt', 'a') as logs:
                        logs.write('ERR MAIN: ' + str({e}))
                    continue
    finally:
        #write the remaining categories in dying_gasp from current line to EOF
        print('PANIC!')
        with open(config['Paths']['evomag_output'] + 'dying_gasp_' + str(currentDate) + '_tmp.txt', 'w') as gasp:
            gasp.write(latest_path + '\n')

            with open(origin, 'r') as origin_file:
                for _ in range(pathCount):
                    origin_file.readline()

                line = origin_file.readline()
                gasp.write(line)
                while(line):
                    line = origin_file.readline()
                    gasp.write(line)
        os.rename(config['Paths']['evomag_output'] + 'dying_gasp_' + str(currentDate) + '_tmp.txt', config['Paths']['evomag_output'] + 'dying_gasp_' + str(currentDate) + '.txt')
        

# scrape('https://www.evomag.ro/telefoane-tablete-accesorii-accesorii-telefoane/filtru/pagina:1')
main()
