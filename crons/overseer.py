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
    host=config['Database']['host'],  
    database=config['Database']['db'],  
    user=config['Database']['user'],  
    password=config['Database']['password']  
)

scripts = [config['Scripts']['evomag_scraper'], config['Scripts']['vexio_scraper']]
processes = []
signals = []

for script in scripts:
        process = subprocess.Popen(['python3', script], stdout=None, stderr=subprocess.DEVNULL)
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

    cur = conn.cursor()

    #create Table for the current day. If the table already exists --> delete it then create it again
    cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' AND tablename LIKE 'products_" + str(datetime.datetime.now().strftime('%Y_%m_%d') + "'"))
    current_table = cur.fetchall()
    
    if current_table:
        print('--->TABLE FOR CURRENT DAY EXISTS --> TRYING TO RECREATE WITH UPDATED VALUES...<---')
        cur.execute("DROP TABLE products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')) + ' CASCADE;')
        conn.commit()
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
    else:
        print('--->TABLE FOR CURRENT DAY DOES NOT EXIST... CREATING TABLE<---')
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
    print('=====SUCCESSFULLY CREATED TABLE FOR CURRENT DAY=====')

    #insert data from .csv files into created table
    copy_statement_evo = "COPY products_2024_09_27(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/evomag/output/evomag_scrape_big.csv' DELIMITER ',' CSV HEADER;"
    copy_statement_vex = "COPY products_2024_09_27(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/vexio/output/vexio_scrape_big.csv' DELIMITER ',' CSV HEADER;"

    with open(config['Paths']['vexio_output'] + "vexio_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_vex, f)
    conn.commit()
    
    with open(config['Paths']['evomag_output'] + "evomag_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_evo, f)
    conn.commit()
    print('=====SUCCESSFULLY INSERTED SCRAPED VALUES INTO CURRENT TABLE=====')

    #delete main table and associated views
    cur.execute("DROP TABLE products CASCADE;")
    conn.commit()
    print('=====SUCCESSFULLY DELETED OLD TABLE AND VIEWS=====')

    #create main table after the current day table
    cur.execute("CREATE TABLE products AS SELECT * FROM products_2024_09_27")
    conn.commit()
    print('=====SUCCESSFULLY CREATED NEW TABLE=====')

    #create views associated to main table
    cur.execute("CREATE VIEW view_products_asc AS SELECT * FROM products ORDER BY raw_price ASC;")
    conn.commit()
    cur.execute("CREATE VIEW view_products_desc AS SELECT * FROM products ORDER BY raw_price DESC;")
    conn.commit()
    print('=====SUCCESSFULLY CREATED NEW VIEWS=====')

    #remove duplicate categories
    print('--->TRYING TO ASSIGN CATEGORIES, THIS MAY TAKE SOME TIME...<---')
    
    cur.execute("SELECT * FROM assign_categories()")
    conn.commit()
    print('=====SUCCESSFULLY ASSIGNED CATEGORIES=====')

    #create price evolution view
    proc_definition = """
    CREATE OR REPLACE PROCEDURE generate_price_history_view()
    LANGUAGE plpgsql
    AS $$
    DECLARE
        select_clause TEXT := 'CREATE OR REPLACE VIEW price_history_view as select products.product_code, ';
        join_clause TEXT;
        i INT;
        table_names TEXT[];
    BEGIN
        SELECT ARRAY(SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname = 'public') INTO table_names;

        FOR i IN 1..array_length(table_names, 1) LOOP
            select_clause := select_clause || ' MIN(' || table_names[i] || '.raw_price) as price_' || table_names[i] || ',';
        END LOOP;

        select_clause := LEFT(select_clause, length(select_clause) - 1);
        select_clause := select_clause || E'\n' || E'FROM products';

        RAISE NOTICE 'select_clause: %', select_clause;

        FOR i IN 1..array_length(table_names, 1) LOOP
            IF table_names[i] NOT LIKE 'products' THEN
                select_clause := select_clause || E'\nFULL OUTER JOIN ' || table_names[i]
                || ' ON products.product_code = ' || table_names[i] || '.product_code';
            END IF;
        END LOOP;

        select_clause := select_clause || E'\nGROUP BY products.product_code;';

        RAISE NOTICE 'select_clause: %', select_clause;
        EXECUTE select_clause;
    END $$;
    """
    cur.execute(proc_definition)
    conn.commit()
    cur.execute('CALL generate_price_history_view();')
    conn.commit()
    print('=====SUCCESSFULLY CREATED price history view=====')


    print('--->DONE!<---')
    cur.close()
    conn.close()
