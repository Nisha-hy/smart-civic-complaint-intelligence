
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_FILE = "bmc_train.csv"
TARGET = "citizen_satisfied"

# Fields excluded from the first model
DROP_COLUMNS = [
    "complaint_id",
    "complaint_date",
    "complaint_status",
    "resolution_days",
    "work_quality_rating",
    TARGET,
]


def prepare_data():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)

    # Separate target and input features
    y = df[TARGET].astype("int8")
    X = df.drop(columns=DROP_COLUMNS)

    # Treat binary target as a classification problem
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\n--- PREPARATION SUMMARY ---")
    print("Total records:", len(df))
    print("Training records:", len(X_train))
    print("Validation records:", len(X_val))
    print("Input features:", X.shape[1])
    print("Training target distribution:")
    print(y_train.value_counts(normalize=True).round(3))

    print("\nTraining and validation split completed.")
    print("No model has been trained yet.")

    return X_train, X_val, y_train, y_val


if __name__ == "__main__":
    prepare_data()

