import psycopg2
import datetime
import csv
import pandas as pd


conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="postgres",  
    password="postgres"  
)

cur = conn.cursor()
cur.execute('SELECT DISTINCT category FROM products')


with open('dataset_laptop' + '.csv', 'w') as dataset:
    cur.execute('SELECT price_products, price_products_2 FROM price_history_view_test WHERE category LIKE ' + "'Laptop & Accesorii'")
    prices = cur.fetchall()
    for price in prices:
        price = str(price).replace(',','').replace('(','').replace(')','').replace("'",'')
        dataset.write(price + '\n')

with open('dataset_laptop_clean.csv', 'a') as dataset:
    with open('dataset_laptop.csv', 'r') as unclean:
        line = unclean.readline()
        while(line):
            line = line.strip().split(' ')
            for i in range(2):
                line[i] = float(line[i])
            if abs(line[0] - line[1]) < 500:
                dataset.write(str(line[0]) + ',' + str(line[1]) + '\n')
            line = unclean.readline()

df = pd.read_csv('dataset_laptop_clean.csv', header=None, names=['Old_Price', 'New_Price'])
# Calculate Q1 (25th percentile) and Q3 (75th percentile)
Q1 = df[['Old_Price', 'New_Price']].quantile(0.25)
Q3 = df[['Old_Price', 'New_Price']].quantile(0.75)

# Compute the Interquartile Range (IQR)
IQR = Q3 - Q1

# Define the outlier step (commonly 1.5 * IQR)
outlier_step = 1.5 * IQR

# Filter the DataFrame to remove outliers
df_filtered = df[~((df[['Old_Price', 'New_Price']] < (Q1 - outlier_step)) | (df[['Old_Price', 'New_Price']] > (Q3 + outlier_step))).any(axis=1)]
df_filtered.to_csv('dataset_laptop_outlierless.csv', index=False)

cur.close()
conn.close()