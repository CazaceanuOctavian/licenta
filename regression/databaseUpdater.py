import psycopg2
import time
import csv
import configparser

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

conn = psycopg2.connect(
    host=config['Database']['host'],  
    database=config['Database']['db'],  
    user=config['Database']['user'],  
    password=config['Database']['password']  
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
