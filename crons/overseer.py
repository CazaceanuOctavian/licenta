import subprocess
import configparser
import time
import signal
import datetime
import psycopg2

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

currentDate = datetime.datetime.now()
start_time = time.time()

#scrape for 28800 seconds (8 hours) at a time
timeout = 28800
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
        cur.execute("CREATE TABLE products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')) + "(\
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
                    predicted_price FLOAT DEFAULT -1,\
                    manufacturer VARCHAR(100) DEFAULT 'N/A'\
                )")
        conn.commit()
    else:
        print('--->TABLE FOR CURRENT DAY DOES NOT EXIST... CREATING TABLE<---')
        cur.execute("CREATE TABLE products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')) + "(\
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
            predicted_price FLOAT DEFAULT -1,\
            manufacturer VARCHAR(100) DEFAULT 'N/A'\
        )")
        conn.commit()
    print('=====SUCCESSFULLY CREATED TABLE FOR CURRENT DAY=====')

    #insert data from .csv files into created table
    copy_statement_evo = "COPY products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')) + "(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/evomag/output/evomag_scrape_big.csv' DELIMITER ',' CSV HEADER;"
    copy_statement_vex = "COPY products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')) + "(name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category) FROM '/home/tav/Desktop/licenta/scraping/vexio/output/vexio_scrape_big.csv' DELIMITER ',' CSV HEADER;"

    with open(config['Paths']['vexio_output'] + "vexio_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_vex, f)
    conn.commit()
    
    with open(config['Paths']['evomag_output'] + "evomag_scrape_big.csv", 'r') as f:
        cur.copy_expert(copy_statement_evo, f)
    conn.commit()
    print('=====SUCCESSFULLY INSERTED SCRAPED VALUES INTO CURRENT TABLE=====')

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
                    WHERE schemaname = 'public' AND tablename LIKE 'products_2%') INTO table_names;

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
    print('=====SUCCESSFULLY UPDATED PRICE HISTORY VIEW=====')

    #create a view with the latest table
    find_latest_table = """
    CREATE OR REPLACE VIEW view_latest_products_table AS 
    SELECT tablename 
    FROM pg_tables 
    WHERE tablename LIKE 'products_2%' 
    ORDER BY tablename DESC 
    LIMIT 1;
    """
    cur.execute(find_latest_table)
    conn.commit()
    print('=====SUCCESSFULLY RETRIEVED TABLE FOR LATEST DAY=====')


    #Create and insert/update into aggregation table all values from old aggregation table(products)
    prepare_insert = """
    CREATE OR REPLACE PROCEDURE insert_into_aggregation_table()
    LANGUAGE plpgsql
    AS $$
    DECLARE
        new_table_name text;
    BEGIN
        SELECT * FROM view_latest_products_table
        INTO new_table_name;

        EXECUTE format('
            CREATE TABLE products_aggregation_table AS
            SELECT n.*
            FROM %I n
            UNION ALL
            SELECT o.*
            FROM products o
            WHERE NOT EXISTS (
                SELECT 1
                FROM %I n
                WHERE n.product_code = o.product_code
            );
        ', new_table_name, new_table_name);
    END $$;
    """

    cur.execute(prepare_insert)
    conn.commit()

    cur.execute("CALL insert_into_aggregation_table()")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM products_aggregation_table")
    sanity_test = cur.fetchall()
    if sanity_test:
        print('=====SUCCESSFULLY INSERTED VALUES INTO AGGREGATION TABLE=====')
    else:
        print("!!!!>-------ERR INSERTING INTO AGGREGATION TABLE!!-------<!!!!")
        raise Exception

    #TODO --> AGREGA AICI PE CATEGORI
    print('--->TRYING TO ASSIGN CATEGORIES, THIS MAY TAKE SOME TIME...<---')
    cur.execute("SELECT * FROM assign_categories()")
    conn.commit()
    print('=====SUCCESSFULLY ASSIGNED CATEGORIES=====')

    #create a table that stores exactly one copy of each product 
    #from products_aggregation_table
    #get the copy that has the lowest price
    create_no_dups_table = """
        CREATE TABLE products_lowest_price_no_dups AS SELECT t1.*
        FROM products_aggregation_table t1
        JOIN (
            SELECT product_code, MIN(raw_price) AS min_price
            FROM products_aggregation_table
            GROUP BY product_code
        ) t2
        ON t1.product_code = t2.product_code
        AND t1.raw_price = t2.min_price;
        """
    
    cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' AND tablename LIKE 'products_lowest_price_no_dups'")
    current_table = cur.fetchall()

    if current_table:
        print('--->NO DUPLICATES AGGREGATION TABLE EXISTS... TRYING TO RECREATE WITH UPDATED VALUES...<---')
        cur.execute("DROP TABLE products_lowest_price_no_dups CASCADE")
        conn.commit()

        cur.execute(create_no_dups_table)
        conn.commit
    else:
        print('--->NO DUPLICATE AGGREGATION TABLE DOES NOT EXIST... CREATING TABLE<---')
        cur.execute(create_no_dups_table)
        conn.commit
    print('=====SUCCESSFULLY CREATED AGGREGATION TABLE WITH NO DUPLICATES=====')


    #remove one of the products that have exactly the same price 
    delete_same_price_dups = """
    DELETE FROM products_lowest_price_no_dups
    WHERE id IN (
        SELECT id
        FROM (
            SELECT MIN(id) as id
            FROM products_lowest_price_no_dups
            WHERE product_code IN (
                SELECT product_code 
                FROM products_lowest_price_no_dups
                GROUP BY product_code
                HAVING COUNT(product_code) > 1
            )
            GROUP BY product_code
        ) as subquery
    );
    """

    cur.execute(delete_same_price_dups)
    conn.commit()
    print('=====SUCCESSFULLY REMOVED PRODUCTS WITH THE SAME PRICE FROM NO DUPLICATES AGGREGATION TABLE=====')

    cur.execute("CREATE OR REPLACE VIEW view_products_asc AS SELECT * FROM products_lowest_price_no_dups ORDER BY raw_price ASC")
    conn.commit()
    cur.execute("CREATE OR REPLACE VIEW view_products_DESC AS SELECT * FROM products_lowest_price_no_dups ORDER BY raw_price DESC")
    conn.commit()
    print('=====SUCCESSFULLY CREATED ORDERING VIEWS=====')


    #drop old aggregation table
    cur.execute("DROP TABLE products CASCADE")
    conn.commit()
    print('=====SUCCESSFULLY REMOVED OLD AGGREGATION TABLE=====')


    #rename new aggregation table to products so that the cycle can begin once more 
    cur.execute("ALTER TABLE products_aggregation_table RENAME TO products")
    conn.commit()
    print('=====SUCCESSFULLY RENAMED CURRENT AGGREGATION TABLE TO PRODUCTS=====')

    #train and predict prices for products by executing predict_prices
    

    print('Done!')
    #delete main table and associated views
    # cur.execute("DROP TABLE products CASCADE;")
    # conn.commit()
    # print('=====SUCCESSFULLY DELETED OLD TABLE AND VIEWS=====')

    # #create main table after the current day table
    # cur.execute("CREATE TABLE products AS SELECT * FROM products_" + str(datetime.datetime.now().strftime('%Y_%m_%d')))
    # conn.commit()
    # print('=====SUCCESSFULLY CREATED NEW TABLE=====')

    # #create views associated to main table
    # cur.execute("CREATE VIEW view_products_asc AS SELECT * FROM products ORDER BY raw_price ASC;")
    # conn.commit()
    # cur.execute("CREATE VIEW view_products_desc AS SELECT * FROM products ORDER BY raw_price DESC;")
    # conn.commit()
    # print('=====SUCCESSFULLY CREATED NEW VIEWS=====')

    # #remove duplicate categories
    # print('--->TRYING TO ASSIGN CATEGORIES, THIS MAY TAKE SOME TIME...<---')
    
    # cur.execute("SELECT * FROM assign_categories()")
    # conn.commit()
    # print('=====SUCCESSFULLY ASSIGNED CATEGORIES=====')

    # #create price evolution view
    # proc_definition = """
    # CREATE OR REPLACE PROCEDURE generate_price_history_view()
    # LANGUAGE plpgsql
    # AS $$
    # DECLARE
    #     select_clause TEXT := 'CREATE OR REPLACE VIEW price_history_view as select products.product_code, ';
    #     join_clause TEXT;
    #     i INT;
    #     table_names TEXT[];
    # BEGIN
    #     SELECT ARRAY(SELECT tablename
    #                 FROM pg_catalog.pg_tables
    #                 WHERE schemaname = 'public') INTO table_names;

    #     FOR i IN 1..array_length(table_names, 1) LOOP
    #         select_clause := select_clause || ' MIN(' || table_names[i] || '.raw_price) as price_' || table_names[i] || ',';
    #     END LOOP;

    #     select_clause := LEFT(select_clause, length(select_clause) - 1);
    #     select_clause := select_clause || E'\n' || E'FROM products';

    #     RAISE NOTICE 'select_clause: %', select_clause;

    #     FOR i IN 1..array_length(table_names, 1) LOOP
    #         IF table_names[i] NOT LIKE 'products' THEN
    #             select_clause := select_clause || E'\nFULL OUTER JOIN ' || table_names[i]
    #             || ' ON products.product_code = ' || table_names[i] || '.product_code';
    #         END IF;
    #     END LOOP;

    #     select_clause := select_clause || E'\nGROUP BY products.product_code;';

    #     RAISE NOTICE 'select_clause: %', select_clause;
    #     EXECUTE select_clause;
    # END $$;
    # """
    # cur.execute(proc_definition)
    # conn.commit()
    # cur.execute('CALL generate_price_history_view();')
    # conn.commit()
    # print('=====SUCCESSFULLY CREATED price history view=====')


    # print('--->DONE!<---')
    # cur.close()
    # conn.close()
