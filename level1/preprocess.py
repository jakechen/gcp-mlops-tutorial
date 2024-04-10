import pandas as pd

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