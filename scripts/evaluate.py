import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score
import boto3
import config
from io import StringIO

def load_test_data():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/processed_data.csv")
    df = pd.read_csv(obj['Body'])
    return df

def evaluate_model():
    model = joblib.load("model.joblib")
    df = load_test_data()
    X_test = df.drop(columns=['SalePrice'])
    y_test = df['SalePrice']
    predictions = model.predict(X_test)
    
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)
    
    print(f"RMSE: {rmse}, R²: {r2}")
    return rmse, r2

evaluate_model()