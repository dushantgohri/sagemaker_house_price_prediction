S3_BUCKET = "your-s3-bucket-name"
S3_PREFIX = "sagemaker/housing"
SNOWFLAKE_USER = "your_user"
SNOWFLAKE_PASSWORD = "your_password"
SNOWFLAKE_ACCOUNT = "your_account"
SNOWFLAKE_WAREHOUSE = "your_warehouse"
SNOWFLAKE_DATABASE = "your_database"
SNOWFLAKE_SCHEMA = "your_schema"
SNOWFLAKE_TABLE = "housing_data"
SNOWFLAKE_PREDICTIONS_TABLE = "predictions"  # Table to store predictions

# Define location filter (Modify as needed)
LOCATION_FILTER = None  # Example: "Downtown" or None for no filtering

# Toggle data source
USE_SNOWFLAKE = True  # Set to False to load from S3 instead

# SageMaker settings
SAGEMAKER_ROLE_ARN = "your-iam-role"
SAGEMAKER_ENDPOINT_NAME = "your-endpoint-name"
