
import pandas as pd

df = pd.read_csv("bmc_train.csv")

df["escalation_risk"] = (
    df["complaint_status"].astype(str).str.strip().str.lower()
    == "escalated"
).astype(int)

print("ESCALATION RATE BY CATEGORY")
print("--------------------------------")

columns = [
    "complaint_category",
    "severity",
    "complaint_channel",
    "zone",
    "ward_type",
    "is_monsoon_season",
]

for col in columns:
    print(f"\n{col.upper()}")

    result = df.groupby(col)["escalation_risk"].agg(
        ["count", "mean"]
    )

    result = result[result["count"] >= 500]
    result["escalation_percentage"] = (
        result["mean"] * 100
    ).round(2)

    print(
        result[["count", "escalation_percentage"]]
        .sort_values("escalation_percentage", ascending=False)
    )



print("\nNUMERIC DATA TYPE INVESTIGATION")
print("--------------------------------")

numeric_columns = [
    "population_density",
    "ward_slum_percentage",
    "prior_complaints_count",
]

for col in numeric_columns:
    print(f"\nCOLUMN: {col}")
    print("Data type:", df[col].dtype)
    print("Non-null values:", df[col].notna().sum())
    print("Missing values:", df[col].isna().sum())

    print("\nSample values:")
    print(df[col].astype(str).value_counts().head(15))

print("\nPOPULATION DENSITY VS ESCALATION")
print("--------------------------------")

result = df.groupby("population_density")[
    "escalation_risk"
].agg(["count", "mean"])

result["escalation_percentage"] = (
    result["mean"] * 100
).round(2)

print(result[["count", "escalation_percentage"]])

