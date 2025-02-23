#!/bin/bash

set -e  # Stop script on error

# Execute SageMaker pipeline
python pipeline.py

# Check pipeline status
aws sagemaker list-pipelines --query "Pipelines[].{Name:PipelineName, Status:PipelineStatus}"