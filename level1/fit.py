# Import the necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from preprocess import preprocess_data
import pickle

# Load the data
df = pd.read_csv('../data/train.csv')

# Preprocess the data
df = preprocess_data(df)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop('Survived', axis=1), df['Survived'], test_size=0.2, random_state=42)

# Train a basic Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create a confusion matrix on the test set
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

# Print the confusion matrix
print(cm)

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)