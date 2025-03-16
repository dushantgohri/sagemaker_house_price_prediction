# ALTER ACCOUNT SET ANACONDA_PACKAGES_ENABLED = TRUE;
# you would need numpy pandas and snowflake

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import StructType, StructField, FloatType, IntegerType
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

import pandas as pd

# Snowflake connection parameters

connection_parameters = {
    "user": "dushantgohri",
    "password": "Dg@17343857148",
    "account": "pwizmma-ka25931",
    "role": "ACCOUNTADMIN",
    "warehouse": "compute_wh",
    "database": "test_datawarehouse",
    "schema": "public"
}

def sum(a, b):

    return a+b



def main(session: Session):

# your own code to dump

    

    print(sum(2,5))
    
    # Load data from Snowflake
    house_data = session.table("DA_DS_HOUSING_V2").to_pandas()
    
    # Data encoding
    encoder = LabelEncoder()
    encoding_col = ['FURNISHINGSTATUS', 'PREFAREA', 'AIRCONDITIONING', 'HOTWATERHEATING', 'BASEMENT', 'GUESTROOM', 'MAINROAD']
    for col in encoding_col:
        house_data[col] = encoder.fit_transform(house_data[col])


    
    # Define features and target
    X = house_data.drop(columns=["PRICE"])
    y = house_data["PRICE"]
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Linear Regression model
    # pkl model file, you can import that 
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Prepare results for Snowflake
    results_df = pd.DataFrame(X_test)
    results_df["PREDICTED_PRICE"] = predictions
    
    # Define schema for the output table
    schema = StructType([
        StructField("PREDICTED_PRICE", FloatType()),
    ])
    
    # Convert DataFrame to Snowpark DataFrame
    snowpark_df = session.create_dataframe(results_df, schema=schema)
    
    # Save predictions back to Snowflake
    snowpark_df.write.mode("overwrite").save_as_table("HOUSE_PRICE_PREDICTIONS")

    # your own code to dump
    
    return snowpark_df


