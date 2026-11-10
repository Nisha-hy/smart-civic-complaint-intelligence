
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. Load the dataset
df = pd.read_csv("bmc_train.csv")

# 2. Define the prediction target
# 1 = escalated, 0 = not escalated
df["escalation_risk"] = (
    df["complaint_status"].astype(str).str.strip().str.lower()
    == "escalated"
).astype(int)

# 3. Select features available at complaint submission
drop_columns = [
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
    "citizen_satisfied",
    "escalation_risk",
]

X = df.drop(columns=drop_columns, errors="ignore")
y = df["escalation_risk"]

# 4. Identify numeric and categorical columns
numeric_features = X.select_dtypes(
    include=["number", "bool"]
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=["number", "bool"]
).columns.tolist()

# 5. Prepare the data
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])

# 6. Build the model
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

# 7. Split and train
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("Training escalation-risk model...")
model.fit(X_train, y_train)

# 8. Evaluate
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\nTarget distribution:")
print(y.value_counts().rename(index={0: "Not escalated", 1: "Escalated"}))

print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Not escalated", "Escalated"],
    zero_division=0,
))

print("ROC-AUC:", round(roc_auc_score(y_test, probabilities), 4))

# 9. Save the model
joblib.dump(model, "civic_escalation_model.joblib")
print("\nSaved: civic_escalation_model.joblib")
