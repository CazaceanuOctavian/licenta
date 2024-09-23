import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

datasetDir = '/home/tavi/Desktop/licenta/regression/dataset/'

for dataset in os.listdir(datasetDir):
    dataset_path = os.path.join(datasetDir, dataset)
    if os.path.isfile(dataset_path):
        data = pd.read_csv(dataset_path)
        if data.empty:
            print(f"Skipping empty dataset: {dataset}")
            with open('/home/tavi/Desktop/licenta/regression/models/performanceLogs.txt', 'a') as logs:
                logs.write(f"WARNING -- DATASET: " + str(dataset) + " is empty!\n")
                logs.write("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
            continue

        X = data[['Old_Price']]  
        y = data['New_Price']    

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

        rf_regressor.fit(X_train, y_train)
        
        y_pred = rf_regressor.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        with open('/home/tavi/Desktop/licenta/regression/models/performanceLogs.txt', 'a') as logs:
            logs.write(f"Performance for category: " + '_'.join(dataset.split('_')[1:])  + '\n') 
            logs.write(f"Mean Squared Error: {mse}" + '\n')
            logs.write(f"R-Squared: {r2}" + '\n')
            logs.write("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")

        with open('/home/tavi/Desktop/licenta/regression/models/' + str(dataset) + '.pkl', 'wb') as file:
             pickle.dump(rf_regressor, file)
    else:
        print('Invalid Path -- ' + str(dataset_path) + ' does not exist')