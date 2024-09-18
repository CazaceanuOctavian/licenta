import psycopg2
import datetime
import csv


conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="postgres",  
    password="postgres"  
)

cur = conn.cursor()
cur.execute('SELECT DISTINCT category FROM products')

categories = cur.fetchall()
formatted_categories = []
for category in categories:
    formatted_categories.append(str(category).replace(',','').replace('(','').replace(')',''))

for category in formatted_categories:
    with open('dataset/category_' + category.replace("'",'') + '.csv', 'a') as dataset:
        cur.execute('SELECT raw_price FROM products WHERE category LIKE ' + str(category))
        prices = cur.fetchall()
        for price in prices:
            price = str(price).replace(',','').replace('(','').replace(')','').replace("'",'')
            dataset.write(price + '\n')
            
cur.close()
conn.close()