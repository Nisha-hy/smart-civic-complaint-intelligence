
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

# Exclude identifiers, the target, and fields that may
# be unavailable when a complaint is first registered.

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
    "TARGET_PLACEHOLDER",
    "months_since_last_maintained",
]


def main():
    # --------------------------------------------------
    # 2. LOAD DATASET
    # --------------------------------------------------

    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)

    # Ensure the target column is not used as an input.
    columns_to_drop = [
        col for col in DROP_COLUMNS
        if col != "TARGET_PLACEHOLDER"
    ]
    columns_to_drop.append(TARGET)

    X = df.drop(columns=columns_to_drop)
    y = df[TARGET].astype("int8")

    # --------------------------------------------------
    # 3. SPLIT DATA
    # --------------------------------------------------

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------
    # 4. IDENTIFY FEATURE TYPES
    # --------------------------------------------------

    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    print("Training records:", len(X_train))
    print("Validation records:", len(X_val))
    print("Numeric features:", len(numeric_features))
    print("Categorical features:", len(categorical_features))

    # --------------------------------------------------
    # 5. PREPROCESSING
    # --------------------------------------------------

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=True,
        )),
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ])

    # --------------------------------------------------
    # 6. RANDOM FOREST MODEL
    # --------------------------------------------------

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            max_depth=16,
            min_samples_leaf=5,
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1,
        )),
    ])

    # --------------------------------------------------
    # 7. TRAIN MODEL
    # --------------------------------------------------

    print("\nTraining Random Forest...")
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, "civic_satisfaction_model.joblib")
    print("Model saved successfully!")

    # --------------------------------------------------
    # 8. PREDICT
    # --------------------------------------------------

    print("Predicting validation records...")
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    # --------------------------------------------------
    # 9. EVALUATE MODEL
    # --------------------------------------------------

    print("\n--- MODEL EVALUATION ---")

    print(
        f"Accuracy: {accuracy_score(y_val, y_pred):.4f}"
    )

    print(
        f"ROC-AUC: {roc_auc_score(y_val, y_prob):.4f}"
    )

    print("\nClassification report:")

    print(classification_report(
        y_val,
        y_pred,
        labels=[0, 1],
        target_names=["Not satisfied", "Satisfied"],
        zero_division=0,
    ))

    print("Confusion matrix:")
    print(confusion_matrix(y_val, y_pred))

    print("\nTraining and evaluation completed.")


if __name__ == "__main__":
    main()
