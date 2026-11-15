
import joblib
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. LOAD TRAINED MODEL
# --------------------------------------------------

MODEL_FILE = "civic_satisfaction_model_19_features_experiment.joblib"

print("Loading trained satisfaction model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully!")


# --------------------------------------------------
# 2. EXTRACT FEATURE IMPORTANCE
# --------------------------------------------------

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

feature_names = preprocessor.get_feature_names_out()
importance_values = classifier.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_values,
})


# --------------------------------------------------
# 3. DISPLAY TOP 15 FEATURES
# --------------------------------------------------

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False,
)

print("\n========== TOP 15 FEATURE IMPORTANCES ==========")

print(
    importance_df.head(15).to_string(index=False)
)


# --------------------------------------------------
# 4. PLOT FEATURE IMPORTANCE
# --------------------------------------------------

top_features = importance_df.head(15).sort_values(
    by="Importance",
    ascending=True,
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"],
)

plt.xlabel("Feature Importance")
plt.ylabel("Input Features")
plt.title("Top 15 Features - Citizen Satisfaction Prediction")

plt.tight_layout()

plt.savefig(
    "satisfaction_feature_importance.png",
    dpi=300,
)

plt.show()

print("\nGraph saved as satisfaction_feature_importance.png")

print("\nFeature importance analysis completed!")
