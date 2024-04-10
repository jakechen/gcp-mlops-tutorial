# Import the necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pickle


def load_data():
    """
    This function loads the Titanic dataset into a Pandas DataFrame.

    Returns:
        A Pandas DataFrame containing the Titanic dataset.
    """
    df = pd.read_csv('../data/train.csv')
    return df

def preprocess_data(df):
    """
    This function preprocesses the Titanic dataset.

    Preprocess the Titanic dataset with the following:
    - Drop Name and ID columns
    - One hot encode pclass, sex, and embarked columns
    - Fill missing values in Age column with the mean

    Args:
        df: A Pandas DataFrame containing the Titanic dataset.

    Returns:
        A preprocessed Pandas DataFrame containing the Titanic dataset.
    """
    # Drop name, id, ticket, and cabin columns
    df = df.drop(['Name', 'PassengerId', 'Ticket', 'Cabin'], axis=1)
    
    # One hot encode pclass, sex, and embarked columns
    df = pd.get_dummies(df, columns=['Pclass', 'Sex', 'Embarked'])
    
    # Fill missing values in Age column with the mean
    df['Age'] = df['Age'].fillna(df['Age'].mean())
    
    return df

def train_and_eval_model(df):
    """
    Train and evaluate model on a train/test split.

    Returns:
        Trained Random Forest model
    """
    # Perform test/train splitting
    X_train, X_test, y_train, y_test = train_test_split(df.drop('Survived', axis=1), df['Survived'], test_size=0.2, random_state=42)

    # Train a basic Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Create a confusion matrix on the test set
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    # Print the confusion matrix
    print(cm)

    return model

# Save the model to GCP GCS bucket

def save_model(model):
    """
    This function saves the trained model and pushes the saved model to GCP GCS bucket.

    Args:
        model: The trained model.

    Returns:
        None
    """

def main():
    """
    This function runs the main program.

    Returns:
        None
    """
    # Load the data
    df = load_data()

    # Preprocess the data
    df = preprocess_data(df)

    # Train and evaluate the model
    model = train_and_eval_model(df)

    # Save the model
    save_model(model)

# Run the main program

if __name__ == '__main__':
    main()