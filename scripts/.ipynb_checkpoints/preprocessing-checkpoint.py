# pip install snowflake-connector-python
import pandas as pd
import sys
# import sagemaker
import boto3
# import snowflake.connector
# sys.path.append('opt/ml/scripts/')

# import config
from io import StringIO
import logging
# from sagemaker.sklearn.model_selection import train_test_split

# Set up logging
logging.basicConfig(
    filename='preprocessing.log',  # Log file path
    level=logging.INFO,            # Log level (INFO or DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_data():
    USE_SNOWFLAKE = False
    if USE_SNOWFLAKE:
        # conn = snowflake.connector.connect(
        #     user=config.SNOWFLAKE_USER,
        #     password=config.SNOWFLAKE_PASSWORD,
        #     account=config.SNOWFLAKE_ACCOUNT
        # )
        # query = f"SELECT * FROM {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.{config.SNOWFLAKE_TABLE}"
        # df = pd.read_sql(query, conn)
        # conn.close()
        print("Loaded data from Snowflake")
    else:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket="sagemaker-us-east-1-237682134737", Key="input_data/housing_data_v2.csv")
        df = pd.read_csv(obj['Body'])
        print("Loaded data from S3")
    return df

def filter_by_location(df):
    if config.LOCATION_FILTER:
        df = df[df['Neighborhood'] == config.LOCATION_FILTER]
        print(f"Filtered data to only include houses in {config.LOCATION_FILTER}")
    return df

def preprocess_data(data):
    """
    Preprocess the input data by handling missing values, encoding categorical variables, 
    and normalizing numerical features.

    Parameters:
    data (pd.DataFrame): The input dataset as a Pandas DataFrame.

    Returns:
    pd.DataFrame: The cleaned and preprocessed DataFrame.
    """
    bedrooms_count = data['bedrooms'].value_counts()
    logging.info(f"bedroom count {bedrooms_count.shape}")

    count_bathrooms = data['bathrooms'].value_counts()
    logging.info(f"bathroom count {count_bathrooms.shape}")

    furnishingstatus_count = data.furnishingstatus.value_counts()
    logging.info(f"finish status of the house {furnishingstatus_count.shape}")

    prefarea_count = data.prefarea.value_counts()
    logging.info(f"pref area count  {prefarea_count.shape}")

    # data encoding
    encoder = LabelEncoder()

    encoding_col = ['furnishingstatus',
                    'prefarea',
                    'airconditioning',
                    'hotwaterheating',
                    'basement',
                    'guestroom',
                    'mainroad']

    for col in encoding_col:
        data[col]=encoder.fit_transform(data[col])

    logging.info(f"getting the shape of the data {data.shape}")
    return data

def save_processed_to_s3(df):
    """
    Save the processed DataFrame to an S3 bucket as a CSV file.

    Parameters:
    df (pd.DataFrame): The processed DataFrame to be saved.
    bucket_name (str): The name of the S3 bucket.
    file_name (str): The name of the file to be saved (e.g., 'processed_data.csv').
    aws_access_key (str, optional): AWS access key (if not using IAM role).
    aws_secret_key (str, optional): AWS secret key (if not using IAM role).
    region_name (str, optional): AWS region (default: 'us-east-1').

    Returns:
    str: Success message if the file is uploaded successfully.
    """
    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.client('s3')
    s3.put_object(Bucket="sagemaker-us-east-1-237682134737", Key="sagemaker/housing_price_prediction/processed_housing_data.csv", Body=csv_buffer.getvalue())
    print("Processed data saved to S3")



def preprocess_data():
    logging.info("Starting data preprocessing...")

    # Example of some preprocessing steps
    try:
        # Example of a function you want to log
        # (Replace with actual preprocessing code)
        logging.info("Loading data...")
        data = load_data()
        data = data.drop('Unnamed: 0',axis=1)

        logging.info(f"head of the data {data.head()}")
        logging.info(f"sample row of the data {data.info()}")
        logging.info(f"describing the data statistics {data.describe()}")

        logging.info(f"getting all the unique value the data statistics {data.nunique()}")
        logging.info(f"getting all the null value from the data {data.isnull()}")
        logging.info(f"getting all the na value the from data {data.isna().sum()}")

        logging.info(f"getting all the sum of the duplicated data {data.duplicated().sum()}")
        logging.info(f"getting the shape of the data {data.shape}")


        # feature and target variable
        x=data.drop(columns=['price'],axis = 1)
        y=data['price']


        # # data splitting
        # x_train, x_test, y_train, y_test=train_test_split(x,
        #                                                   y,
        #                                                   test_size=0.25,
        #                                                   random_state=50)

        # logging.info(f"getting the shape of the x_train {x_train.shape}")
        # logging.info(f"getting the shape of the x_test {x_test.shape}")
        # logging.info(f"getting the shape of the y_train {y_train.shape}")
        # logging.info(f"getting the shape of the y_test {y_test.shape}")


        # data = load_data()  # Uncomment and replace with actual data loading function
        logging.info("Data loaded successfully.")

        logging.info("Performing data cleaning...")
        # processed_data = preprocess_data(data)

        # logging.info(f"head of the prepocessing data {processed_data.head()}")

        # clean_data()  # Uncomment and replace with actual cleaning function
        logging.info("Data cleaned successfully.")

        logging.info("Saving the data to s3...")
        save_processed_to_s3(data)

        logging.info("saved the data to s3...")

    except Exception as e:
        logging.error(f"Error occurred during preprocessing: {e}")
        raise  # Optionally re-raise the error if you want the pipeline to fail

def main():

    # S3_BUCKET = "sagemaker-us-east-1-237682134737"
    # S3_PREFIX = "sagemaker/housing_price_prediction"
    
    preprocess_data()

if __name__ == "__main__":
    main()


