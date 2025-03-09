import sagemaker
from sagemaker.sklearn import SKLearn
import config

s3_input = f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/processed_data.csv"
output_path = f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/model"

sklearn_estimator = SKLearn(entry_point='train_script.py', 
                            role=config.SAGEMAKER_ROLE_ARN,
                            instance_type='ml.m5.large',
                            framework_version='0.23-1',
                            script_mode=True,
                            output_path=output_path)

sklearn_estimator.fit({'train': s3_input})