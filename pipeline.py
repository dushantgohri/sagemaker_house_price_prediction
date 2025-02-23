from sagemaker.workflow.steps import ProcessingStep, TrainingStep, TransformStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator
from sagemaker.transformer import Transformer

session = PipelineSession()


# Define preprocessing step
preprocessing_processor = ScriptProcessor(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-processing:0.23-1-cpu-py3",
    role="your-iam-role",
    instance_count=1,
    instance_type="ml.m5.large"
)

preprocessing_step = ProcessingStep(
    name="PreprocessData",
    processor=preprocessing_processor,
    inputs=[],
    outputs=[],
    code="scripts/preprocessing.py"
)

# Define training step
training_estimator = Estimator(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-training:0.23-1-cpu-py3",
    role="your-iam-role",
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/model"
)

training_step = TrainingStep(
    name="TrainModel",
    estimator=training_estimator,
    inputs={"train": f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/processed_data.csv"}
)

# Define evaluation step
evaluation_processor = ScriptProcessor(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-processing:0.23-1-cpu-py3",
    role="your-iam-role",
    instance_count=1,
    instance_type="ml.m5.large"
)

evaluation_step = ProcessingStep(
    name="EvaluateModel",
    processor=evaluation_processor,
    inputs=[],
    outputs=[],
    code="scripts/evaluate.py"
)

# Define inference step
transformer = Transformer(
    model_name="your-model-name",
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/inference"
)

inference_step = TransformStep(
    name="Inference",
    transformer=transformer,
    inputs={"input": f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/test_data.csv"}
)


condition_step = ConditionStep(name="CheckModelQuality",
    conditions=[ConditionGreaterThanOrEqualTo(left=evaluation_step.properties.Outputs['RMSE'], right=0.1)],
    if_steps=[training_step],
    else_steps=[])


pipeline = Pipeline(
    name="HousingPricePredictionPipeline",
    parameters=[],
    steps=[preprocessing_step, training_step, evaluation_step, condition_step, inference_step]
)

pipeline.upsert(role_arn='your-iam-role')
