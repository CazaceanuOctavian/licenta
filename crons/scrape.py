import subprocess
import configparser
import sys
import time
import signal
import datetime
import psycopg2

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

currentDate = datetime.datetime.now()
start_time = time.time()

#scrape for 28800 seconds (8 hours) at a time
timeout = 10
last_print_time = 0  

conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="tav",  
    password="qwe123"  
)

scripts = [config['Scripts']['evomag_scraper'], config['Scripts']['vexio_scraper']]
processes = []
signals = []

for script in scripts:
        process = subprocess.Popen(['python3', script], stdout=None, stderr=None)
        processes.append(process)
        signals.append(process.pid)

try:
    print(str(currentDate) + ' --> SCRAPING STARTED SUCCESFULLY')
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= timeout:
            print("8 hours have passed! Terminating all processes...")
            break

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected! Terminating all processes...")


#TODO --> REMOVE HARDCODING AFTER YOU GET ENOUGH DATA
finally:
    #send KeyboardInterrupt signal to terminate processes gracefully
    for process in processes:
        if process.poll() is None:  
            process.send_signal(signal.SIGINT)

    #create Table for the current day
    cur = conn.cursor()
    cur.execute('CREATE TABLE products_' + str(datetime.datetime.now().strftime('%Y_%m_%d')) + '(\
        id SERIAL PRIMARY KEY,\
        name VARCHAR(500),\
        raw_price FLOAT,\
        raw_rating INTEGER,\
        is_in_stock BOOLEAN,\
        url VARCHAR(500),\
        product_code VARCHAR(100),\
        retailer VARCHAR(100),\
        imagepath VARCHAR(150),\
        category VARCHAR(150),\
        predicted_price FLOAT DEFAULT -1\
    )')
    conn.commit()

    #insert data from .csv files into created table
    copy_statement_evo = "COPY products_2024_09_27(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/evomag/output/evomag_scrape_big.csv' DELIMITER ',' CSV HEADER;"
    copy_statement_vex = "COPY products_2024_09_27(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/vexio/output/vexio_scrape_big.csv' DELIMITER ',' CSV HEADER;"

    with open(config['Paths']['vexio_output'] + "vexio_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_vex, f)
    conn.commit()
    
    with open(config['Paths']['evomag_output'] + "evomag_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_evo, f)
    conn.commit()

    #delete main table and associated views
    cur.execute("DROP TABLE products CASCADE;")
    conn.commit()

    #create main table after the current day table
    cur.execute("CREATE TABLE products AS SELECT * FROM products_2024_09_27")
    conn.commit()

    #create views
    cur.execute("CREATE VIEW view_products_asc AS SELECT * FROM products")
    conn.commit()
    cur.execute("CREATE VIEW view_products_asc AS SELECT * FROM products")
    conn.commit()

    cur.close()
    conn.close()


