
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Civic Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Civic Analytics & Decision Support")
st.write(
    "Explore complaint patterns, citizen satisfaction, "
    "and resolution performance using the dataset."
)

DATA_FILE = "bmc_train.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, low_memory=False)

    # Convert columns to numeric where appropriate.
    for col in [
        "citizen_satisfied",
        "resolution_days",
        "year",
        "month",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "bmc_train.csv was not found. "
        "Place it in the same folder as analytics.py."
    )
    st.stop()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()


required_columns = [
    "complaint_category",
    "citizen_satisfied",
    "resolution_days",
    "year",
    "month",
    "zone",
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()


# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.header("Analytics Filters")

filtered_df = df.copy()

years = sorted(
    filtered_df["year"].dropna().unique().tolist()
)

if years:
    selected_years = st.sidebar.multiselect(
        "Select year(s)",
        options=years,
        default=years,
    )

    if selected_years:
        filtered_df = filtered_df[
            filtered_df["year"].isin(selected_years)
        ]
    else:
        filtered_df = filtered_df.iloc[0:0]


zones = sorted(
    filtered_df["zone"].dropna().astype(str).unique()
)

if zones:
    selected_zones = st.sidebar.multiselect(
        "Select zone(s)",
        options=zones,
        default=zones,
    )

    if selected_zones:
        filtered_df = filtered_df[
            filtered_df["zone"].astype(str).isin(
                selected_zones
            )
        ]
    else:
        filtered_df = filtered_df.iloc[0:0]


if filtered_df.empty:
    st.warning(
        "No records match these filters. "
        "Select at least one year and one zone."
    )
    st.stop()


# -------------------------------
# KEY PERFORMANCE INDICATORS
# -------------------------------

total_complaints = len(filtered_df)

satisfaction = (
    filtered_df["citizen_satisfied"].dropna()
)

if len(satisfaction) > 0:
    satisfaction_rate = (
        satisfaction.eq(1).mean() * 100
    )
else:
    satisfaction_rate = None

resolution = (
    filtered_df["resolution_days"].dropna()
)

if len(resolution) > 0:
    average_resolution = resolution.mean()
else:
    average_resolution = None


st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Complaints",
    f"{total_complaints:,}",
)

col2.metric(
    "Citizen Satisfaction Rate",
    (
        f"{satisfaction_rate:.1f}%"
        if satisfaction_rate is not None
        else "N/A"
    ),
)

col3.metric(
    "Average Resolution Time",
    (
        f"{average_resolution:.1f} days"
        if average_resolution is not None
        else "N/A"
    ),
)

st.caption(
    "These are descriptive statistics from historical "
    "dataset records, not future predictions."
)

st.divider()



# -------------------------------
# CHART 1: COMPLAINT CATEGORIES
# -------------------------------

import altair as alt

st.subheader("1. Most Common Complaint Categories")

category_counts = (
    filtered_df["complaint_category"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
    .rename_axis("Complaint Category")
    .reset_index(name="Number of Complaints")
    .sort_values("Number of Complaints")
)

category_chart = alt.Chart(category_counts).mark_bar().encode(
    x=alt.X(
        "Number of Complaints:Q",
        title="Number of Complaints",
        axis=alt.Axis(format=","),
    ),
    y=alt.Y(
        "Complaint Category:N",
        sort=None,
        title="Complaint Category",
        axis=alt.Axis(labelLimit=260),
    ),
    tooltip=[
        "Complaint Category",
        alt.Tooltip("Number of Complaints:Q", format=","),
    ],
).properties(height=360)

st.altair_chart(category_chart, use_container_width=True)


# -------------------------------
# CHART 2: COMPLAINT TRENDS
# -------------------------------

st.subheader("2. Complaint Trends Over Time")

monthly = filtered_df.dropna(
    subset=["year", "month"]
).copy()

monthly["year"] = monthly["year"].astype(int)
monthly["month"] = monthly["month"].astype(int)

monthly = monthly[
    monthly["month"].between(1, 12)
]

monthly["Period"] = (
    monthly["year"].astype(str)
    + "-"
    + monthly["month"].astype(str).str.zfill(2)
)

trend = (
    monthly.groupby("Period")
    .size()
    .sort_index()
    .rename("Complaints")
)

if not trend.empty:
    st.line_chart(trend)
else:
    st.info("No valid year/month records for this chart.")


# -------------------------------
# CHART 3: SATISFACTION BY ZONE
# -------------------------------

st.subheader("3. Satisfaction Rate by Zone")

zone_data = filtered_df.dropna(
    subset=["zone", "citizen_satisfied"]
).copy()

if not zone_data.empty:
    zone_rates = (
        zone_data.groupby("zone")["citizen_satisfied"]
        .apply(lambda values: values.eq(1).mean() * 100)
        .sort_values(ascending=False)
    )

    st.bar_chart(zone_rates)
else:
    st.info("No satisfaction data available for this chart.")



# -------------------------------
# CHART 4: RESOLUTION TIME
# -------------------------------

st.subheader("4. Resolution Time Distribution")

valid_resolution = resolution[resolution >= 0]

if not valid_resolution.empty:
    median_days = valid_resolution.median()
    percentile_95 = valid_resolution.quantile(0.95)

    col1, col2 = st.columns(2)
    col1.metric("Median Resolution Time", f"{median_days:.1f} days")
    col2.metric("95th Percentile", f"{percentile_95:.1f} days")

    # Show the main distribution without allowing extreme
    # values to compress the majority of the observations.
    chart_data = valid_resolution[
        valid_resolution <= percentile_95
    ]

    histogram = (
        pd.cut(chart_data, bins=20, include_lowest=True)
        .value_counts()
        .sort_index()
        .rename_axis("Resolution Time Range")
        .reset_index(name="Number of Complaints")
    )

    histogram["Resolution Time Range"] = (
        histogram["Resolution Time Range"].astype(str)
    )

    st.bar_chart(
        histogram.set_index("Resolution Time Range")
        ["Number of Complaints"]
    )

    st.caption(
        "The distribution excludes records above the 95th "
        "percentile for display. Those records remain in the "
        "dataset and are not deleted."
    )
else:
    st.info("No valid resolution-time records available.")


# -------------------------------
# DATA PREVIEW
# -------------------------------

with st.expander("View filtered dataset preview"):
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
    )

    st.caption(
        f"Showing up to 100 of {len(filtered_df):,} "
        "filtered records."
    )

st.divider()

st.caption(
    "Educational prototype. Historical patterns do not "
    "establish causation or guarantee future outcomes."
)

st.subheader("Escalation Target Investigation")

st.write("Complaint status counts:")

status_counts = df["complaint_status"].value_counts(
    dropna=False
).reset_index()

status_counts.columns = ["Complaint Status", "Count"]

st.dataframe(status_counts, use_container_width=True)

st.write("Available complaint-related columns:")
st.write([
    col for col in df.columns
    if any(word in col.lower() for word in [
        "escalat", "status", "reassign", "resolution"
    ])
])
