
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

DATA_FILE = "bmc_train.csv"

MODEL_FILE = (
    "civic_satisfaction_model_19_features_experiment.joblib"
)

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


# --------------------------------------------------
# 2. LOAD DATASET AND MODEL
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_FILE, low_memory=False)

print("Dataset loaded:", df.shape)

print("\nLoading trained model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully!")


# --------------------------------------------------
# 3. PREPARE INPUT AND TARGET
# --------------------------------------------------

X = df.drop(
    columns=[
        col for col in DROP_COLUMNS + [TARGET]
        if col in df.columns
    ]
)

y = pd.to_numeric(
    df[TARGET],
    errors="raise"
).astype("int8")


# --------------------------------------------------
# 4. RECREATE VALIDATION SPLIT
# --------------------------------------------------

print("\nPreparing validation dataset...")

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("Validation records:", len(X_val))


# --------------------------------------------------
# 5. BASELINE PERFORMANCE
# --------------------------------------------------

print("\nCalculating original model performance...")

y_prob = model.predict_proba(X_val)[:, 1]

baseline_auc = roc_auc_score(y_val, y_prob)

print(f"Original ROC-AUC: {baseline_auc:.4f}")


# --------------------------------------------------
# 6. PERMUTATION IMPORTANCE
# --------------------------------------------------

print("\nCalculating permutation importance...")

print("This may take several minutes.")

result = permutation_importance(
    model,
    X_val,
    y_val,
    scoring="roc_auc",
    n_repeats=3,
    random_state=42,
    n_jobs=1,
)

print("Permutation analysis completed!")


# --------------------------------------------------
# 7. CREATE RESULTS TABLE
# --------------------------------------------------

importance_df = pd.DataFrame({
    "Feature": X_val.columns,
    "Importance": result.importances_mean,
    "Standard Deviation": result.importances_std,
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False,
)

print("\n========== PERMUTATION IMPORTANCE ==========")

print(
    importance_df.to_string(index=False)
)


# --------------------------------------------------
# 8. SAVE RESULTS
# --------------------------------------------------

importance_df.to_csv(
    "satisfaction_permutation_importance.csv",
    index=False,
)

print("\nResults saved successfully!")


# --------------------------------------------------
# 9. VISUALIZE TOP 15 FEATURES
# --------------------------------------------------

top_features = importance_df.head(15).sort_values(
    by="Importance",
    ascending=True,
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"],
    xerr=top_features["Standard Deviation"],
    capsize=3,
)

plt.xlabel("Decrease in ROC-AUC after shuffling")
plt.ylabel("Input Features")

plt.title(
    "Permutation Importance - Citizen Satisfaction Prediction"
)

plt.axvline(x=0, linestyle="--")

plt.tight_layout()

plt.savefig(
    "satisfaction_permutation_importance.png",
    dpi=300,
)

plt.show()

print("\nGraph saved successfully!")

print("\nAnalysis completed!")
