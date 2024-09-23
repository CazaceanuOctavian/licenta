import psycopg2
import pandas as pd
import os
import configparser


conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="postgres",  
    password="postgres"  
)

cur = conn.cursor()
cur.execute('SELECT DISTINCT category FROM products')

config = configparser.ConfigParser()
config.read('/home/tavi/Desktop/licenta/cfg.ini')

categories = cur.fetchall()
formatted_categories = []
for category in categories:
    formatted_categories.append(str(category).replace(',','').replace('(','').replace(')',''))

for category in formatted_categories:
    try:
        with open(config['Paths']['dataset_path'] + 'dts_' + category.replace("'",'').replace(' ','_') + '_tmp.csv', 'a') as dataset:
            cur.execute('SELECT price_products, price_products_2 FROM price_history_view_test WHERE category LIKE ' + str(category))
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