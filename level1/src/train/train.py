# Import the necessary libraries
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the data
iris = load_iris()

# Train a basic Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(iris.data, iris.target)

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Training completed.")