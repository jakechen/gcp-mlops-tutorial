import os
import pickle
from google.cloud import storage
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


# Load the data
iris = load_iris()

# Train a basic Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(iris.data, iris.target)

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Push saved model to GCS bucket
storage_client = storage.Client()
bucket = storage_client.bucket(os.environ['AIP_MODEL_DIR'])
blob = bucket.blob('model.pkl')
blob.upload_from_filename('model.pkl')

print("Training completed.")