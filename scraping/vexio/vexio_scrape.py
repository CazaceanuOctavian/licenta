import re
import os
import csv
import requests
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import NavigableString
from bs4 import BeautifulSoup

options = Options()
#options.add_argument('--headless')
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
        price = float(item.find_next(class_='price margin-bottom-xs clearfix col-xs-6 grid-full').text.strip().replace(',','.').split(' ')[0])
        itemUrl = item.find_parent().findPreviousSibling().a['href']
        #explodes here when there are no valid images
        imageUrl = item.find_parent().findPreviousSibling().find_next('img')['data-src']

        driver.delete_all_cookies()
        driver.get(itemUrl)
        page_source = driver.page_source
        other_soup = BeautifulSoup(page_source, 'html.parser')

        product_code = other_soup.find(class_='model').text.strip()
        print(name)

        #=====scraping image=====
        try:
            img_data = requests.get(imageUrl).content
            img_name = product_code + '.jpeg'
            #
            filepath = os.path.join('/home/tavi/Desktop/licenta/frontend/public/images', img_name) 
            with open(filepath, 'wb') as file:
                file.write(img_data)
        except Exception as e:
            print('could not get image, so sad...')
            filepath = 'err'
        #=====scraping image=====

        return {
            'name' : name,
            'raw_price' : price,
            'raw_rating' : -1,
            'is_in_stoc' : isInStoc,
            'url' : itemUrl,
            'product_code' : product_code,
            'online_mag' : 'vexio',
            'img_path' : '/images/' + img_name
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

        # last_url = driver.current_url
        
        li_items = soup.find_all(class_="grid-full col-xs-8 col-sm-4 col-md-4")
        category = soup.find(class_='breadcrumb').text.strip().split('\xa0')[-1]
        next_page_button = soup.find(class_ = 'pagination-next')

        #done here because images on product page are too high quality
        #wait 2 seconds on each large page to make images load --> replace with wait-until(selenium) at some point...
        # time.sleep(2)
        # #=====scraping image=====
        # li_images = soup.find_all(class_="margin-bottom-xs grid-full image text-center col-xs-4 col-sm-3 col-md-3")
        # counter = 0
        # for image in li_images:
        #     imageUrl = image.find_next('img')['data-src']
        #     try:
        #         img_data = requests.get(imageUrl).content
        #         img_name = str(counter)
        #         #
        #         filepath = os.path.join('/home/tavi/Desktop/licenta/content', img_name) 
        #         with open(filepath, 'wb') as file:
        #             file.write(img_data)
        #         counter+=1
        #     except Exception as e:
        #         print('could not get image, so sad...')
        #         filepath = 'err'
        # #=====scraping image=====

        with open('vexio_scrape_jpgs.csv', 'a', newline='') as scrapefile:
                writer = csv.writer(scrapefile)
                for element in li_items:
                    try:
                        element = no_nav_strings(element.descendants)
                        formatted_dict = format_data(element[0])
                        formatted_dict['category'] = category

                        writer.writerow(formatted_dict.values())
                    except Exception as e:
                        print(str({e}))
                        break

        if (next_page_button == None):
            break
                
        new_path = path + 'pagina' + str(current_page) + '/'
        driver.delete_all_cookies()
        driver.get(new_path)

        # url_test = driver.current_url

        # if last_url == url_test:
        #     break
           
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



#scrape('https://www.vexio.ro/laptop-accesorii/pagina503/')

main()
driver.quit()