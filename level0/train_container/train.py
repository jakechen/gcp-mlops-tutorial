import os
import pickle
from google.cloud import storage
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import datetime

# Load the data
iris = load_iris()

# Train a basic Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(iris.data, iris.target)

# Save the model to a file
model_filename = 'model.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Set the bucket name
bucket_name = 'spatial-tempo-418521'  # Name of the bucket

# Access the bucket
bucket = storage_client.bucket(bucket_name)

# Create a blob object from the filename
TIMESTAMP=datetime.datetime.now().strftime('%Y%m%d%H%M%S')

blob = bucket.blob(f"model-{TIMESTAMP}/model.pkl")

# Upload the file to Google Cloud Storage
blob.upload_from_filename(model_filename)

