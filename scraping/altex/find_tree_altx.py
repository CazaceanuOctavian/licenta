import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup


options = Options()

options.binary_location = '/etc/firefox'

driver = webdriver.Firefox(options=options)
start_url = "https://altex.ro/home/"
driver.get(start_url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
html_content = soup.prettify()
with open('htmldump.txt', 'w') as file:
    file.write(html_content)

li_items = soup.find_all(class_=re.compile("pr-4", re.IGNORECASE))

#unreadeable ass code >:(
with open('ALTEX_Tree.txt', 'w') as file:
     for element in li_items:
        children = list(element.children)   
        if len(children) == 1:
            file.write(children[0].get('href') + '\n')
        else:
            element_list = list(children[1].children)
            for elem_item in element_list:
                final_children = list(elem_item.children)
                for fin_child in final_children:
                    if fin_child.get('href') is not None:
                        file.write(fin_child.get('href') + '\n')

driver.quit()