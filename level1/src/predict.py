import pandas as pd
from preprocess import preprocess_data
import pickle

# Load the data
df = pd.read_csv('../data/test.csv')

# Preprocess the data
df = preprocess_data(df)

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict with model
y_pred = model.predict(df)
print(y_pred[:5])