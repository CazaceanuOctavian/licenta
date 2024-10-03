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

driver = create_driver()
driver.get("https://www.evomag.ro/portabile-accesorii-laptop-componente-laptop/seagate-hdd-laptop-seagate-barracuda-st500lm030-500gb-5400rpm-sata-3-2.5-128mb-2912869.html")
page_source = driver.page_source
other_soup = BeautifulSoup(page_source, 'html.parser')



em_elems = other_soup.find(class_='product_info_area').find_all_previous('em')
print(em_elems[1].text.strip())

# em_elems = other_soup.find('div', attrs={'class': 'breadcrumbs productpage'}).find_next('div').find_all_previous('em')
# em_list = [em.contents for em in em_elems if em != "\n" and "»" not in em]

# print(em_list[-1].text)
# if em_elems[-1].text == '*Specificatiile pot varia de la un model #pentru ca nu vreau sa fac is pe primele 3 coloanela altul in functie de configuratie':
#     em_elems.remove(em_elems[-1])
# manufacturer = em_elems[-2].text.strip().lower()

driver.quit()