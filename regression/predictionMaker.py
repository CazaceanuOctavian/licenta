import psycopg2
import pandas as pd
import pickle
import os
import time



conn = psycopg2.connect(
    host="localhost",  
    database="product_administration",  
    user="postgres",  
    password="postgres"  
)

def predict_price(Old_Price, loaded_model):
    input_data = pd.DataFrame([[Old_Price]], columns=['Old_Price'])
    predicted_price = loaded_model.predict(input_data)
    return predicted_price[0]  

cur = conn.cursor()
cur.execute('SELECT DISTINCT category FROM products')

categories = cur.fetchall()
formatted_categories = []
for category in categories:
    formatted_categories.append(str(category).replace(',','').replace('(','').replace(')',''))

for category in formatted_categories:
    try:
        #TODO --> shit naming, make it not shitty by removing .csv
        model_path = 'models/dts_' + category.replace("'",'').replace(' ','_') + '.csv.pkl'
        print('trying to predict with model ' + model_path)
        try:
            with open(model_path, 'rb') as model_file:
                model = pickle.load(model_file)
        except Exception as e:
            print('WARNING -- Did not find valid model for path: ' + model_path)
            continue
        
        cur.execute('SELECT id, raw_price FROM products WHERE category LIKE ' + category)
        fetchedItems = cur.fetchall()

        with open('predictions/output_test.csv', 'a') as output:
            for item in fetchedItems:
                item_id = item[0]
                item_price = item[1]
                output.write(str(item_id) + ',' + str(predict_price(item_price, model)) + '\n')
    except Exception as e:
        print('Something went wrong...' + str({e}))
        continue

cur.close()
conn.close()