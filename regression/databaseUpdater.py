import psycopg2
import time
import csv

conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="postgres",  
    password="postgres"  
)

cur = conn.cursor()
start_time = time.time()
print('Updating...')
with open('predictions/output_test.csv', 'r') as predictions:
    line = predictions.readline()
    while(line):
        line = line.split(',')
        product_id = line[0]
        predicted_price = line[1]
        
        cur.execute('UPDATE products SET predicted_price = ' + str(predicted_price) + ' WHERE id = ' + str(product_id))
        conn.commit()

        line = predictions.readline()

uptime = time.time() - start_time
print('Update process finished succesfully in: ' + str(uptime) + ' seconds')
