import argparse
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def model_fn(model_dir):
    """Load the trained model for inference."""
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

if __name__ == "__main__":
    # SageMaker passes hyperparameters as command-line arguments
    parser = argparse.ArgumentParser()

    # SageMaker training input and output directories
    parser.add_argument("--train-data", type=str, default="/opt/ml/input/data/train")  
    parser.add_argument("--model-dir", type=str, default="/opt/ml/model")  

    args = parser.parse_args()

    # Load training data
    data_path = os.path.join(args.train_data, "train.csv")  # Assuming CSV format
    df = pd.read_csv(data_path)

    # Assuming the last column is the target variable
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    print(f"Validation MSE: {mse}")
    r2 = r2_score(y_val, y_pred)

    # Save the trained model to the model directory
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))




        # # models
        # ln_model = LinearRegression()
        # ln_model.fit(x_train, y_train)

        # y_pred = ln_model.predict(x_test)

        # ln_acc = r2_score(y_test, y_pred)
        # ln_acc

        # # AdaBoostRegressor

        # abr_model = AdaBoostRegressor()
        # abr_model.fit(x_train, y_train)

        # y_pred = abr_model.predict(x_test)

        # abr_acc = r2_score(y_test, y_pred)
        # abr_acc

