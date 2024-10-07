import psycopg2
import pandas as pd
import os
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

conn = psycopg2.connect(
    host=config['Database']['host'],  
    database=config['Database']['db'],  
    user=config['Database']['user'],  
    password=config['Database']['password']  
)

cur = conn.cursor()
cur.execute('SELECT DISTINCT category FROM products')

categories = cur.fetchall()
formatted_categories = []
for category in categories:
    formatted_categories.append(str(category).replace(',','').replace('(','').replace(')',''))

for category in formatted_categories:
    try:
        with open(config['Paths']['dataset_path'] + 'dts_' + category.replace("'",'').replace(' ','_') + '_tmp.csv', 'a') as dataset:
            #get all columns for dataset 
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name LIKE 'price_history_view' AND column_name LIKE 'price_%' ORDER BY column_name DESC")
            columns = cur.fetchall()
            for i in range(len(columns)):
                columns[i] = str(columns[i]).replace("'", '').replace('(','').replace(')','').replace(',','')
            #filter columns so that we chose them based on a time interval starting with the latest scraped date
            selected_columns = []
            i=0
            while i < len(columns):
                current_column = columns[i]
                selected_columns.append(current_column)
                found_match = False
                for j in range(i+1, len(columns)):
                    next_column = columns[j]
                    current_date = datetime.strptime(current_column[-10:], '%Y_%m_%d')
                    next_date = datetime.strptime(next_column[-10:], '%Y_%m_%d')
                    difference = (current_date - next_date).days
                    #change here to get the desired number of days
                    if (difference >= 7):
                        i = j 
                        found_match = True
                        break
                if found_match is False:
                    break
            #stringify resulting vector so that we can use it in a SELECT query  
            resulting_columns = ','.join(selected_columns)

            cur.execute('SELECT' + resulting_columns + 'FROM price_history_view_test WHERE category LIKE ' + str(category))
            prices = cur.fetchall()
            for price in prices:
                price = str(price).replace(',','').replace('(','').replace(')','').replace("'",'')  
                price = price.strip().split(' ')
                for i in range(2):
                    price[i] = float(price[i])
                if abs(price[0] - price[1]) < 500:
                    dataset.write(str(price[0]) + ',' + str(price[1]) + '\n')

        df = pd.read_csv(config['Paths']['dataset_path'] + 'dts_' + category.replace("'",'').replace(' ','_') + '_tmp.csv', header=None, names=['Old_Price', 'New_Price'])
        Q1 = df[['Old_Price', 'New_Price']].quantile(0.25)
        Q3 = df[['Old_Price', 'New_Price']].quantile(0.75)

        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR

        df_filtered = df[~((df[['Old_Price', 'New_Price']] < (Q1 - outlier_step)) | (df[['Old_Price', 'New_Price']] > (Q3 + outlier_step))).any(axis=1)]
        df_filtered.to_csv(config['Paths']['dataset_path'] +'dts_' + category.replace("'",'').replace(' ','_') + '.csv', index=False)

        os.remove(config['Paths']['dataset_path'] + 'dts_' + category.replace("'",'').replace(' ','_') + '_tmp.csv')
    except Exception as e:
        print('Someting went wrong: ' + str({e}))

cur.close()
conn.close()