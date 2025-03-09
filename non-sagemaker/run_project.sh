#!/bin/bash

set -e  # Stop script on error

# Get the current directory path
CURRENT_DIR=$(pwd)

# Set the necessary variables
# S3_BUCKET="s3://sagemaker-us-east-1-237682134737/src/"

SOURCE_DIR="$CURRENT_DIR"  # Using the current directory
PIPELINE_SCRIPT="scripts/preprocessing.py"  # Assuming the pipeline.py is in the current directory

# Step 0: Install the required packages
echo "Installing required packages..."
pip install -r requirements.txt


# Step 1: Copy the entire directory to S3 bucket
# echo "Copying directory to S3..."
# aws s3 cp $SOURCE_DIR $S3_BUCKET --recursive

# Step 2: Run the pipeline Python script
echo "Running SageMaker pipeline script..."
python3 $PIPELINE_SCRIPT

# Step 3: Check the status
if [ $? -eq 0 ]; then
  echo "Pipeline executed successfully."
else
  echo "Error occurred while executing the pipeline."
fi
