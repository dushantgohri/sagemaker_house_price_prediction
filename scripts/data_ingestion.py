import snowflake.connector
import pandas as pd
import boto3
import config
from io import StringIO

def fetch_data():
    conn = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        account=config.SNOWFLAKE_ACCOUNT
    )
    query = f"SELECT * FROM {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.{config.SNOWFLAKE_TABLE}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def save_to_s3(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/raw_data.csv", Body=csv_buffer.getvalue())
    print("Data saved to S3")

data = fetch_data()
save_to_s3(data)