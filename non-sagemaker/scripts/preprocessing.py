# pip install snowflake-connector-python
import pandas as pd
import sys
import boto3
import os
# import snowflake.connector
# sys.path.append('opt/ml/scripts/')

# import config
from io import StringIO
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Set up logging
logging.basicConfig(
    filename='preprocessing.log',  # Log file path
    level=logging.INFO,            # Log level (INFO or DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data_csv():


    file_path = os.path.join(os.path.dirname(__file__), '../data/housing_data_v2.csv')
    print(f"file path {file_path}")
    logging.info(f"file path {file_path}")
    df = pd.read_csv(file_path)
    
    logging.info("Loaded data from csv")
    return df


# def load_data():
#     USE_SNOWFLAKE = False
#     if USE_SNOWFLAKE:
#         conn = snowflake.connector.connect(
#             user=config.SNOWFLAKE_USER,
#             password=config.SNOWFLAKE_PASSWORD,
#             account=config.SNOWFLAKE_ACCOUNT
#         )
#         query = f"SELECT * FROM {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.{config.SNOWFLAKE_TABLE}"
#         df = pd.read_sql(query, conn)
#         conn.close()
#         logging.info("Loaded data from Snowflake")
#     else:
#         s3 = boto3.client('s3')
#         obj = s3.get_object(Bucket="sagemaker-us-east-1-237682134737", Key="input_data/housing_data_v2.csv")
#         df = pd.read_csv(obj['Body'])
#         logging.info("Loaded data from S3")
#     return df

# def filter_by_location(df):
#     if config.LOCATION_FILTER:
#         df = df[df['Neighborhood'] == config.LOCATION_FILTER]
#         print(f"Filtered data to only include houses in {config.LOCATION_FILTER}")
#     return df

def preprocess_data(data):
    """
    Preprocess the input data by handling missing values, encoding categorical variables, 
    and normalizing numerical features.

    Parameters:
    data (pd.DataFrame): The input dataset as a Pandas DataFrame.

    Returns:
    pd.DataFrame: The cleaned and preprocessed DataFrame.
    """

    data.columns = [col.lower() for col in data.columns]  # Convert all headers to lowercase

    # Example of a function you want to log
        # (Replace with actual preprocessing code)
    logging.info("Data loaded successfully.")

    logging.info("Performing data cleaning...")
    logging.info(f"head of the data {data.head()}")
    logging.info(f"sample row of the data {data.info()}")
    logging.info(f"describing the data statistics {data.describe()}")

    logging.info(f"getting all the unique value the data statistics {data.nunique()}")
    logging.info(f"getting all the null value from the data {data.isnull()}")
    logging.info(f"getting all the na value the from data {data.isna().sum()}")

    logging.info(f"getting all the sum of the duplicated data {data.duplicated().sum()}")
    logging.info(f"getting the shape of the data {data.shape}")


    logging.info("Data cleaned successfully.")
    
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
    logging.info(f"getting the head of the data {data.head()}")
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



def train_model(df):
    logging.info("Starting model training...")

    try:
        # Split the data into features and target variable
        X = df.drop(columns=['price'])
        y = df['price']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=50)

        logging.info(f"Shape of X_train: {X_train.shape}")
        logging.info(f"Shape of X_test: {X_test.shape}")
        logging.info(f"Shape of y_train: {y_train.shape}")
        logging.info(f"Shape of y_test: {y_test.shape}")

        # Initialize and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate and log the mean squared error
        mse = mean_squared_error(y_test, y_pred)
        logging.info(f"Mean Squared Error on test set: {mse}")

    except Exception as e:
        logging.error(f"Error occurred during model training: {e}")
        raise  # Optionally re-raise the error if you want the pipeline to fail

    return model


# def save_predictions_to_snowflake():

#     conn = snowflake.connector.connect(
#         user=config.SNOWFLAKE_USER,
#         password=config.SNOWFLAKE_PASSWORD,
#         account=config.SNOWFLAKE_ACCOUNT
#     )

#     query = f"INSERT INTO {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}.{config.SNOWFLAKE_TABLE} VALUES (?, ?, ?, ?)"
#     cursor = conn.cursor()

#     for i in range(len(df)):
#         cursor.execute(query, (df['ID'][i], df['price'][i], y_pred[i], '2021-09-01'))

#     conn.commit()
#     conn.close()

#     logging.info("Predictions saved to Snowflake")

def main():

    # df = load_data()
    df = load_data_csv()
    
    pre_process_df = preprocess_data(df)

    model_trained = train_model(pre_process_df)

    # save_predictions_to_snowflake(df, model_trained)

    # evaluate_model(df)






if __name__ == "__main__":
    main()


