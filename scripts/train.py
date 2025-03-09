import sagemaker
# from sagemaker.sklearn import SKLearn
import config

from sagemaker.sklearn.preprocessing import LabelEncoder
from sagemaker.sklearn.preprocessing import StandardScaler, MinMaxScaler
from sagemaker.sklearn.model_selection import train_test_split

from SKLsagemaker.sklearnearn.linear_model import LinearRegression
from sagemaker.sklearn.tree import DecisionTreeRegressor
from sagemaker.sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor

from sagemaker.sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score

s3_input = f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/processed_data.csv"
output_path = f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/model"

sklearn_estimator = SKLearn(entry_point='train_model.py', 
                            role=config.SAGEMAKER_ROLE_ARN,
                            instance_type='ml.m5.large',
                            framework_version='0.23-1',
                            script_mode=True,
                            output_path=output_path)

sklearn_estimator.fit({'train': s3_input})

