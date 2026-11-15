
import pandas as pd
import joblib
import gc

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

EXPERIMENT_B_FEATURES = [
    "year",
    "month",
    "ward_code",
    "ward_area",
    "zone",
    "population_density",
    "ward_slum_percentage",
    "complaint_category",
    "complaint_channel",
    "has_photo_evidence",
    "has_gps_location",
    "complainant_type",
    "property_type",
]


# --------------------------------------------------
# 2. BUILD MODEL
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
# 3. RUN ONE EXPERIMENT
# --------------------------------------------------

def run_experiment(
    experiment_name,
    X_train,
    X_val,
    y_train,
    y_val,
    model_file,
):

    print("\n" + "=" * 55)
    print(experiment_name)
    print("=" * 55)

    print("Number of input features:", X_train.shape[1])

    model = build_model(X_train)

    print("\nTraining model...")

    model.fit(X_train, y_train)

    print("Training completed!")

    print("\nGenerating predictions...")

    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    accuracy = accuracy_score(y_val, y_pred)
    roc_auc = roc_auc_score(y_val, y_prob)

    print("\n========== EVALUATION RESULTS ==========")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

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

    print("\nSaving experiment model...")

    joblib.dump(model, model_file)

    print("Saved as:", model_file)

    del model
    gc.collect()

    return {
        "Experiment": experiment_name,
        "Features": X_train.shape[1],
        "Accuracy": accuracy,
        "ROC-AUC": roc_auc,
    }


# --------------------------------------------------
# 4. MAIN
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

    # One shared split for a fair comparison
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\nTraining records:", len(X_train))
    print("Validation records:", len(X_val))

    # Experiment A: all 19 features
    result_A = run_experiment(
        "EXPERIMENT A - 19 FEATURES",
        X_train,
        X_val,
        y_train,
        y_val,
        "civic_satisfaction_model_19_features_experiment.joblib",
    )

    # Experiment B: selected 13 features
    X_train_B = X_train[EXPERIMENT_B_FEATURES]
    X_val_B = X_val[EXPERIMENT_B_FEATURES]

    result_B = run_experiment(
        "EXPERIMENT B - 13 FEATURES",
        X_train_B,
        X_val_B,
        y_train,
        y_val,
        "civic_satisfaction_model_13_features_experiment.joblib",
    )

    # Final comparison
    print("\n" + "=" * 65)
    print("FINAL MODEL COMPARISON")
    print("=" * 65)

    comparison = pd.DataFrame([result_A, result_B])

    print(comparison.to_string(index=False))

    print("\nBoth experiments completed successfully!")


if __name__ == "__main__":
    main()
