import pandas as pd
import boto3
import snowflake.connector
import config
from io import StringIO

def load_data():
    if config.USE_SNOWFLAKE:
        conn = snowflake.connector.connect(
            user=config.SNOWFLAKE_USER,
            password=config.SNOWFLAKE_PASSWORD,
            account=config.SNOWFLAKE_ACCOUNT
        )
        query = f"SELECT * FROM {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.{config.SNOWFLAKE_TABLE}"
        df = pd.read_sql(query, conn)
        conn.close()
        print("Loaded data from Snowflake")
    else:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/raw_data.csv")
        df = pd.read_csv(obj['Body'])
        print("Loaded data from S3")
    return df

def filter_by_location(df):
    if config.LOCATION_FILTER:
        df = df[df['Neighborhood'] == config.LOCATION_FILTER]
        print(f"Filtered data to only include houses in {config.LOCATION_FILTER}")
    return df

def preprocess_data(df):
    df = filter_by_location(df)
    df.fillna(df.median(), inplace=True)
    return df

def save_processed_to_s3(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/processed_data.csv", Body=csv_buffer.getvalue())
    print("Processed data saved to S3")

data = load_data()
processed_data = preprocess_data(data)
save_processed_to_s3(processed_data)
