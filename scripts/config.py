S3_BUCKET = "sagemaker-us-east-1-237682134737"
S3_PREFIX = "sagemaker/housing_price_prediction"
train_S3_PREFIX = "input_data"


SNOWFLAKE_USER = "dushantgohri"
SNOWFLAKE_PASSWORD = "Dg@17343857148"
SNOWFLAKE_ACCOUNT = "pwizmma-ka25931"
SNOWFLAKE_WAREHOUSE = "compute_wh"
SNOWFLAKE_DATABASE = "test_datawarehouse"
SNOWFLAKE_SCHEMA = "public"
SNOWFLAKE_TABLE = "DA_DS_HOUSING_PRICE_TRAIN_TBL"
SNOWFLAKE_PREDICTIONS_TABLE = "predictions"  # Table to store predictions


# Define location filter (Modify as needed)
LOCATION_FILTER = None  # Example: "Downtown" or None for no filtering

# Toggle data source
USE_SNOWFLAKE = False  # Set to False to load from S3 instead

# SageMaker settings
SAGEMAKER_ROLE_ARN = "arn:aws:iam::237682134737:role/awsSagemaker_fullaccess_DG"
SAGEMAKER_ENDPOINT_NAME = "your-endpoint-name"