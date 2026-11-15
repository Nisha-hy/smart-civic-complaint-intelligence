
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

BASELINE_MODEL = (
    "civic_satisfaction_model_19_features_experiment.joblib"
)

REDUCED_MODEL = (
    "civic_satisfaction_model_7_features_experiment.joblib"
)

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

SELECTED_FEATURES = [
    "has_photo_evidence",
    "is_monsoon_season",
    "complaint_channel",
    "has_gps_location",
    "complaint_category",
    "ward_type",
    "severity",
]


# --------------------------------------------------
# 2. BUILD RANDOM FOREST MODEL
# --------------------------------------------------

def build_model(X_train):

    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=True,
            ),
        ),
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ])

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
            ),
        ),
    ])

    return model


# --------------------------------------------------
# 3. EVALUATE MODEL
# --------------------------------------------------

def evaluate_model(name, model, X_val, y_val):

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    y_pred = model.predict(X_val)

    y_prob = model.predict_proba(X_val)[:, 1]

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
            target_names=["Not satisfied", "Satisfied"],
            zero_division=0,
        )
    )

    print("Confusion Matrix:")

    print(confusion_matrix(y_val, y_pred))

    return {
        "Model": name,
        "Features": X_val.shape[1],
        "Accuracy": accuracy,
        "ROC-AUC": roc_auc,
    }


# --------------------------------------------------
# 4. MAIN PROGRAM
# --------------------------------------------------

def main():

    print("Loading dataset...")

    df = pd.read_csv(DATA_FILE, low_memory=False)

    print("Dataset shape:", df.shape)

    X = df.drop(
        columns=[
            col for col in DROP_COLUMNS + [TARGET]
            if col in df.columns
        ]
    )

    y = pd.to_numeric(
        df[TARGET],
        errors="raise",
    ).astype("int8")

    # Recreate the original shared split
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
    # EXPERIMENT A: EXISTING 19-FEATURE MODEL
    # --------------------------------------------------

    print("\nLoading 19-feature baseline model...")

    baseline_model = joblib.load(BASELINE_MODEL)

    result_A = evaluate_model(
        "EXPERIMENT A - 19 FEATURES",
        baseline_model,
        X_val,
        y_val,
    )

    del baseline_model

    # --------------------------------------------------
    # EXPERIMENT B: NEW 7-FEATURE MODEL
    # --------------------------------------------------

    print("\nPreparing selected 7 features...")

    X_train_B = X_train[SELECTED_FEATURES]
    X_val_B = X_val[SELECTED_FEATURES]

    print("Selected features:", SELECTED_FEATURES)

    print("\nBuilding 7-feature model...")

    model_B = build_model(X_train_B)

    print("Training 7-feature model...")

    model_B.fit(X_train_B, y_train)

    print("Training completed!")

    result_B = evaluate_model(
        "EXPERIMENT B - 7 FEATURES",
        model_B,
        X_val_B,
        y_val,
    )

    print("\nSaving 7-feature model...")

    joblib.dump(model_B, REDUCED_MODEL)

    print("Saved as:", REDUCED_MODEL)

    # --------------------------------------------------
    # 5. FINAL COMPARISON
    # --------------------------------------------------

    print("\n" + "=" * 65)
    print("FINAL MODEL COMPARISON")
    print("=" * 65)

    comparison = pd.DataFrame([result_A, result_B])

    print(comparison.to_string(index=False))

    print("\nBoth experiments completed successfully!")


if __name__ == "__main__":
    main()
