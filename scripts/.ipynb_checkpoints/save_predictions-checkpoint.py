pip install snowflake-connector-python
import snowflake.connector
import pandas as pd
import config
from io import StringIO

def save_predictions_to_snowflake(predictions):
    conn = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        account=config.SNOWFLAKE_ACCOUNT
    )
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.predictions (
            Id INT PRIMARY KEY,
            SalePrice FLOAT
        )
    """)
    
    for index, row in predictions.iterrows():
        cursor.execute(f"""
            INSERT INTO {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.predictions (Id, SalePrice)
            VALUES ({row['Id']}, {row['SalePrice']})
        """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Predictions saved to Snowflake")

def save_to_s3(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=config.S3_BUCKET, Key=f"{config.S3_PREFIX}/raw_data.csv", Body=csv_buffer.getvalue())
    print("Data saved to S3")

data = fetch_data()
save_to_s3(data)