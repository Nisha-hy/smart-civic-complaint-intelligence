
import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    classification_report
)


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

DATA_FILE = "bmc_train.csv"

FEATURES = [
    "year",
    "month",
    "is_monsoon_season",
    "complaint_time_of_day",
    "ward_code",
    "ward_area",
    "zone",
    "ward_type",
    "population_density",
    "ward_slum_percentage",
    "complaint_category",
    "complaint_channel",
    "severity",
    "has_photo_evidence",
    "has_gps_location",
    "complainant_type",
    "property_type",
    "repeat_complainant",
    "prior_complaints_count"
]

TARGET = "citizen_satisfied"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

X = df[FEATURES]
y = df[TARGET].astype(int)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

print("\nTarget distribution:")
print(y.value_counts())


# --------------------------------------------------
# 3. TRAIN-VALIDATION SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Validation records:", len(X_test))


# --------------------------------------------------
# 4. PREPROCESSING
# --------------------------------------------------

numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            SimpleImputer(strategy="median"),
            numeric_features
        ),
        (
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True
                ))
            ]),
            categorical_features
        )
    ]
)


# --------------------------------------------------
# 5. DEFINE ALGORITHMS
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        solver="saga",
        max_iter=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "SGD Classifier": SGDClassifier(
        loss="log_loss",
        max_iter=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=16,
        min_samples_leaf=5,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    )
}


# --------------------------------------------------
# 6. TRAIN AND EVALUATE
# --------------------------------------------------

results = []

for name, model in models.items():

    print("\n" + "=" * 55)
    print("TRAINING:", name)
    print("=" * 55)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    start_time = time.time()

    pipeline.fit(X_train, y_train)

    training_time = time.time() - start_time

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    balanced_accuracy = balanced_accuracy_score(
        y_test, predictions
    )
    precision = precision_score(
        y_test, predictions, zero_division=0
    )
    recall = recall_score(
        y_test, predictions, zero_division=0
    )
    f1 = f1_score(
        y_test, predictions, zero_division=0
    )
    roc_auc = roc_auc_score(y_test, probabilities)
    pr_auc = average_precision_score(y_test, probabilities)

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Not Satisfied", "Satisfied"],
        zero_division=0
    ))

    print("Accuracy:", round(accuracy, 4))
    print("Balanced Accuracy:", round(balanced_accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1 Score:", round(f1, 4))
    print("ROC-AUC:", round(roc_auc, 4))
    print("PR-AUC:", round(pr_auc, 4))
    print("Training Time:", round(training_time, 2), "seconds")

    results.append({
        "Algorithm": name,
        "Accuracy": accuracy,
        "Balanced Accuracy": balanced_accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
        "Training Time (seconds)": training_time
    })


# --------------------------------------------------
# 7. FINAL COMPARISON
# --------------------------------------------------

results_df = pd.DataFrame(results)

print("\n\n")
print("=" * 75)
print("FINAL ALGORITHM COMPARISON")
print("=" * 75)

print(
    results_df.sort_values(
        by="ROC-AUC",
        ascending=False
    ).to_string(index=False)
)

results_df.to_csv(
    "satisfaction_algorithm_comparison.csv",
    index=False
)

print("\nComparison saved to satisfaction_algorithm_comparison.csv")
print("\nAlgorithm comparison completed!")
