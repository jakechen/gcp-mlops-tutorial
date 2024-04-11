import numpy as np
import pandas as pd
import json
import datetime

import tensorflow as tf

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline


def get_data(url,target):
    # Load the dataset
    df = pd.read_csv(url)

    # Drop the ID column
    df.drop('ID', axis=1, inplace=True)
    
    categorical_features = df.drop('Profit', axis=1).columns.tolist()
    numerical_feature = []

    
    label=df[target]
    data= df[categorical_features+numerical_feature]
    
    return label, data,categorical_features,numerical_feature
    
def pre_processing(label, data,categorical_features,numerical_feature):
    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median'))
                                      ,('scaler', StandardScaler())])
    categorical_transformer = OneHotEncoder(categories='auto')

    encoder = ColumnTransformer(
    transformers=[
        ('numerical', numeric_transformer, numerical_feature),
        ('categorical', categorical_transformer, categorical_features)])
    
    encoder.fit(data)
    return encoder, label, data,categorical_features,numerical_feature

#Model selection function
def regressor_selection(X,y, metric = 'r2'):    
    pipe = Pipeline([('regressor' , RandomForestRegressor())])    
    param_grid = ''
    param = [        
                
        {'regressor' : [RandomForestRegressor()],
        'regressor__n_estimators' : [200,500],
        'regressor__max_depth' : list( range(5,25,5) ),
        'regressor__min_samples_split' : list( range(4,12,2) )
        },
        
        {'regressor' : [KNeighborsRegressor()],
         'regressor__n_neighbors' : [5,10,20],
         'regressor__p' : [1,2] 
        },
        {
         'regressor' : [Lasso(max_iter=500)],
         'regressor__alpha' : [0.01,0.1,1,10]         
        }
            ]
    param_grid = param    
    clf = GridSearchCV(pipe, param_grid = param_grid, 
                       cv = 2, n_jobs=-1,scoring = metric)    
    best_clf = clf.fit(X, y)
    
    return(best_clf.best_params_['regressor'])

def run_model():
    url = 'https://github.com/AmirMK/DataHour/raw/main/Restaurant_Profitability_Training_Data.csv'
    target = 'Profit'
        
    label, data,categorical_features,numerical_feature = get_data(url,target)
    
    encoder, label, data,categorical_features,numerical_feature = pre_processing(label, data,categorical_features,numerical_feature)
    
    
    clf = regressor_selection(encoder.transform(data),label, metric = 'r2')
    
    
    model = clf.fit(encoder.transform(data),label)
    
    
    prediction_model = make_pipeline(encoder,model)
    
    
    url = 'https://github.com/AmirMK/DataHour/raw/main/Restaurant_Profitability_Training_Data.csv'
    df = pd.read_csv(url)

    new_data = df.head(10)
    new_data.drop('ID', axis=1, inplace=True)
    new_data.drop('Profit', axis=1, inplace=True)
    
    result = prediction_model.predict(new_data)
    result_list = result.tolist()
    result_data = {'prediction': result_list}
    result_json = json.dumps(result_data)
    
    TIMESTAMP=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    FILE_NAME = "prediction_result-{}.json".format(TIMESTAMP)

    BUCKET_URI = 'gs://spatial-tempo-418521/prediction_result'
    gcs_input_uri = BUCKET_URI + "/" + FILE_NAME
    
    with tf.io.gfile.GFile(gcs_input_uri, 'w') as f:
        f.write(result_json)
    
    
    return 1
    
