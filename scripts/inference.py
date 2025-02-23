import boto3
import pandas as pd
import config

def load_test_data():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/test_data.csv")
    df = pd.read_csv(obj['Body'])
    return df

def invoke_sagemaker_endpoint(endpoint_name, data):
    runtime = boto3.client('sagemaker-runtime')
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='text/csv',
        Body=data.to_csv(index=False, header=False)
    )
    predictions = response['Body'].read().decode('utf-8').splitlines()
    return predictions

def save_predictions(predictions, test_data):
    test_data['SalePrice'] = predictions
    save_predictions_to_snowflake(test_data)

test_data = load_test_data()
predictions = invoke_sagemaker_endpoint("your-endpoint-name", test_data)
save_predictions(predictions, test_data)