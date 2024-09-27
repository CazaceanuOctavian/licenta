import psycopg2
import datetime
import time

conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="tav",  
    password="qwe123"  
)

cur = conn.cursor()
cur.execute('CREATE TABLE products_' + str(datetime.datetime.now().strftime('%Y_%m_%d')) + ' AS SELECT * FROM PRODUCTS WHERE 1 = 2')
conn.commit()
cur.close()
conn.close()
