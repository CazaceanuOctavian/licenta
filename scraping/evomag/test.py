import re
import json
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import NavigableString
from bs4 import BeautifulSoup
options = Options()

options.binary_location = '/etc/firefox'

driver = webdriver.Firefox(options=options)

driver.get('https://www.evomag.ro/portabile-accesorii-laptop/filtru/pagina:2')

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

for script in soup(["script", "noscript"]):
    script.extract()

pag1_html = soup.prettify()

driver.get('https://www.evomag.ro/portabile-accesorii-laptop')
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

for script in soup(["script", "noscript"]):
    script.extract()

pag2_html = soup.prettify()

if pag1_html == pag2_html:
    print('true!')



print()