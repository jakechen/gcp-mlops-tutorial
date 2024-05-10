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
print("Model fit complete")

# Save the model
with open("model.pkl", 'wb') as f:
    pickle.dump(model, f)
print("Model saved to GCS")

# Upload model artifact to Cloud Storage
model_directory = 'gs://mlops-maturity-tutorial-level0'
storage_path = os.path.join(model_directory, 'model.pkl')
blob = storage.blob.Blob.from_string(storage_path, client=storage.Client())
blob.upload_from_filename('model.pkl')
print("Model artifact pushed")

print("Training completed.")