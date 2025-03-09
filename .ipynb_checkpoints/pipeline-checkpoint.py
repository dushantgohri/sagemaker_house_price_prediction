import config
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, TransformStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator
from sagemaker.transformer import Transformer
from sagemaker.processing import ProcessingOutput, ProcessingInput
from sagemaker import get_execution_role
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.properties import PropertyFile
from sagemaker.processing import ScriptProcessor
from sagemaker.workflow.utilities import PipelineDefinitionConfig

session = PipelineSession()

# Define a ScriptProcessor
preprocessing_processor = ScriptProcessor(
    image_uri="683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3",
    role=config.SAGEMAKER_ROLE_ARN,
    instance_count=1,
    instance_type="ml.m5.large",
    command=["python3"],  # Define command here instead of ProcessingStep
)

# Define the ProcessingStep
preprocessing_step = ProcessingStep(
    name="PreprocessData",
    processor=preprocessing_processor,
    inputs=[
        ProcessingInput(
            source=f"s3://{config.S3_BUCKET}/src/scripts/preprocessing.py",
            destination="/opt/ml/processing/input"
        )
    ],
    # outputs=[
    #     ProcessingOutput(
    #         source="/opt/ml/processing/output",
    #         destination=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/processed_data.csv",
    #         output_name="processed_data"
    #     )
    # ],
    code="scripts/preprocessing.py"  # Ensure this file exists and is correctly referenced
)



# Define training step
training_estimator = Estimator(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-training:0.23-1-cpu-py3",
    role=config.SAGEMAKER_ROLE_ARN,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/model"
)


training_step = TrainingStep(
    name="TrainModel",
    estimator=training_estimator,
    inputs={"train": f"s3://{config.S3_BUCKET}/scripts/train.py"}
)


# Define evaluation step
evaluation_processor = ScriptProcessor(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-processing:0.23-1-cpu-py3",
    role=config.SAGEMAKER_ROLE_ARN,
    instance_count=1,
    instance_type="ml.m5.large"
)


# evaluation_step = ProcessingStep(
#     name="EvaluateModel",
#     processor=evaluation_processor,
#     inputs=[ProcessingInput(
#         source=training_step.properties.ModelArtifacts["S3ModelArtifacts"],
#         destination="/opt/ml/processing/model"
#     )],
#     outputs=[ProcessingOutput(
#         source="/opt/ml/processing/output",
#         destination=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/metrics",
#         output_name="metrics"
#     )],
#     code="scripts/evaluate.py"
# )


# Define inference step
transformer = Transformer(
    model_name="houseprediction",
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/inference"
)

inference_step = TransformStep(
    name="Inference",
    transformer=transformer,
    inputs={"input": f"s3://{config.S3_BUCKET}/{config.S3_PREFIX}/test_data.csv"}
)


# condition_step = ConditionStep(
#     name="CheckModelQuality",
#     conditions=[ConditionGreaterThanOrEqualTo(
#         left=evaluation_step.properties.ProcessingOutputConfig.Outputs["metrics"].S3Uri,
#         right="0.1"
#     )],
#     if_steps=[inference_step],
#     else_steps=[]
# )


# Define the pipeline
# pipeline = Pipeline(
#     name="MySageMakerPipeline",
#     steps=[preprocessing_step],
#     # Use PipelineDefinitionConfig to persist ProcessingJobName in the pipeline definition if required
#     pipeline_definition_config=PipelineDefinitionConfig(
#         persist_processing_job_name=True
#     )
# )




pipeline = Pipeline(
    name="HousingPricePredictionPipeline",
    parameters=[],
    steps=[preprocessing_step,
           # training_step,
           # evaluation_step,
           # condition_step,
           # inference_step
          ],
    # Use PipelineDefinitionConfig to persist ProcessingJobName in the pipeline definition if required
    # pipeline_definition_config=PipelineDefinitionConfig(
    #     persist_processing_job_name=True
    # )
)

pipeline.upsert(role_arn=config.SAGEMAKER_ROLE_ARN)
# Execute pipeline

pipeline.start()