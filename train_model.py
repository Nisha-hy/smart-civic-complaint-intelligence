
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

DATA_FILE = "bmc_train.csv"
TARGET = "citizen_satisfied"
MODEL_FILE = "civic_satisfaction_model.joblib"

DROP_COLUMNS = [
    "complaint_id",
    "complaint_date",
    "complaint_status",
    "resolution_days",
    "num_reassignments",
    "department_assigned",
    "media_attention",
    "politically_sensitive",
    "contractor_category",
    "work_quality_rating",
    "site_inspected",
    "defect_liability_claim",
    "estimated_cost_inr",
    "infrastructure_age_years",
    "months_since_last_maintained",
]


def main():

    # --------------------------------------------------
    # 2. LOAD DATASET
    # --------------------------------------------------

    print("Loading dataset...")

    df = pd.read_csv(DATA_FILE, low_memory=False)

    print("Dataset loaded successfully!")
    print("Dataset shape:", df.shape)

    if TARGET not in df.columns:
        raise ValueError(
            f"Target column '{TARGET}' not found."
        )

    # --------------------------------------------------
    # 3. PREPARE INPUT AND TARGET
    # --------------------------------------------------

    columns_to_drop = [
        col for col in DROP_COLUMNS
        if col in df.columns
    ]

    X = df.drop(columns=columns_to_drop + [TARGET])
    y = pd.to_numeric(
        df[TARGET], errors="raise"
    ).astype("int8")

    # --------------------------------------------------
    # 4. FEATURE AUDIT
    # --------------------------------------------------

    print("\n========== FEATURE AUDIT ==========")

    print("\nInput features used by the model:")
    print(X.columns.tolist())

    print("\nNumber of input features:", len(X.columns))

    print("\nTarget distribution:")
    print(y.value_counts().sort_index())

    print("\nTarget percentages:")
    print(
        (y.value_counts(normalize=True).sort_index() * 100)
        .round(2)
    )

    print("\n===================================")

    # --------------------------------------------------
    # 5. SPLIT DATASET
    # --------------------------------------------------

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\nTraining records:", len(X_train))
    print("Validation records:", len(X_val))

    # --------------------------------------------------
    # 6. IDENTIFY FEATURE TYPES
    # --------------------------------------------------

    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    print("\nNumeric features:", len(numeric_features))
    print("Categorical features:", len(categorical_features))

    # --------------------------------------------------
    # 7. PREPROCESSING
    # --------------------------------------------------

    numeric_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
    ])

    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=True,
            )
        ),
    ])

    preprocessor = ColumnTransformer([
        (
            "numeric",
            numeric_pipeline,
            numeric_features,
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features,
        ),
    ])

    # --------------------------------------------------
    # 8. RANDOM FOREST MODEL
    # --------------------------------------------------

    model = Pipeline([
        ("preprocessor", preprocessor),

        (
            "classifier",
            RandomForestClassifier(
                n_estimators=100,
                max_depth=16,
                min_samples_leaf=5,
                class_weight="balanced_subsample",
                random_state=42,
                n_jobs=-1,
            )
        ),
    ])

    # --------------------------------------------------
    # 9. TRAIN MODEL
    # --------------------------------------------------

    print("\nTraining Random Forest model...")

    model.fit(X_train, y_train)

    print("Training completed!")

    # --------------------------------------------------
    # 10. PREDICTION
    # --------------------------------------------------

    print("\nPredicting validation records...")

    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    # --------------------------------------------------
    # 11. MODEL EVALUATION
    # --------------------------------------------------

    print("\n========== MODEL EVALUATION ==========")

    accuracy = accuracy_score(y_val, y_pred)

    roc_auc = roc_auc_score(y_val, y_prob)

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_val,
            y_pred,
            labels=[0, 1],
            target_names=[
                "Not satisfied",
                "Satisfied",
            ],
            zero_division=0,
        )
    )

    print("Confusion Matrix:")

    print(confusion_matrix(y_val, y_pred))

    # --------------------------------------------------
    # 12. SAVE MODEL
    # --------------------------------------------------

    joblib.dump(model, MODEL_FILE)

    print("\nModel saved successfully!")
    print("Model file:", MODEL_FILE)

    print("\nTraining and evaluation completed.")


if __name__ == "__main__":
    main()
