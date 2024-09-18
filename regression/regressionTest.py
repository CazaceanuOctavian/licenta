#thank you gipiti
#/==================\#
# Import necessary libraries
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the CSV data
data = pd.read_csv('dataset_laptop_clean.csv', header=None, names=['old_price', 'new_price'])

# Define the features (X) and target (y)
X = data[['old_price']]  # Old price is the input feature
y = data['new_price']    # New price is the target

# Split data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model on the training data
rf_regressor.fit(X_train, y_train)

# Save the model to a file using pickle
with open('models/testCategory.pkl', 'wb') as file:
    pickle.dump(rf_regressor, file)

# Load the saved model (in case you want to load it later)
with open('models/testCategory.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Make predictions on the test set to evaluate the model
y_pred = loaded_model.predict(X_test)

# Evaluate the model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

print("=====================")

# Function to predict new price based on user input
def predict_new_price(old_price):
    # Convert the input to a pandas DataFrame with the same format as the training data
    input_data = pd.DataFrame([[old_price]], columns=['old_price'])
    
    # Use the loaded model to make a prediction
    predicted_price = loaded_model.predict(input_data)
    
    return predicted_price[0]  # Return the single predicted value

# Example of how you can use the function with a user-provided price
user_old_price = float(input("Enter the old price: "))
predicted_new_price = predict_new_price(user_old_price)
print(f"The predicted new price is: {predicted_new_price}")
