
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F5F2EA;
    }

    [data-testid="stSidebar"] {
        background-color: #101B2D;
    }

    [data-testid="stSidebar"] * {
        color: #F5F2EA;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #101B2D;
    }

    h1, h2, h3 {
        color: #101B2D;
    }

    .portal-banner {
        background: linear-gradient(110deg, #101B2D, #263C50);
        border-bottom: 5px solid #C5A15B;
        padding: 28px 32px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
    }

    .portal-kicker {
        color: #D8BD83;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .portal-title {
        color: #FFFFFF;
        font-size: 29px;
        font-weight: 750;
        margin: 9px 0 5px 0;
    }

    .portal-subtitle {
        color: #E3E8ED;
        font-size: 14px;
        margin: 0;
    }

    .portal-tagline {
        color: #D8BD83;
        font-size: 13px;
        font-style: italic;
        margin-top: 17px;
    }

    .section-heading {
        color: #101B2D;
        font-size: 21px;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #647181;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-top: 4px solid #C5A15B;
        border-radius: 10px;
        padding: 19px 20px;
        min-height: 116px;
        box-shadow: 0 3px 12px rgba(16, 27, 45, 0.045);
    }

    .kpi-label {
        color: #647181;
        font-size: 12px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .kpi-value {
        color: #101B2D;
        font-size: 27px;
        font-weight: 750;
        margin-top: 9px;
    }

    .kpi-note {
        color: #87909A;
        font-size: 11px;
        margin-top: 4px;
    }

    .info-panel {
        background: #FFFFFF;
        border-left: 4px solid #C5A15B;
        border-radius: 7px;
        padding: 13px 17px;
        color: #526071;
        font-size: 13px;
        margin: 12px 0 20px 0;
    }

    .footer-panel {
        background: #101B2D;
        color: #DDE3E9;
        padding: 17px 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 12px;
        margin-top: 24px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E5E0D5;
        border-radius: 9px;
        padding: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #647181;
    }

    div[data-testid="stMetricValue"] {
        color: #101B2D;
    }

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #E5E0D5;
        border-radius: 8px;
    }

    .stButton button {
        background-color: #101B2D;
        color: white;
        border: 1px solid #C5A15B;
        border-radius: 7px;
    }

    .stButton button:hover {
        background-color: #263C50;
        color: white;
        border-color: #C5A15B;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E5E0D5;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PORTAL HEADER
# --------------------------------------------------

st.html("""
<div class="portal-banner">
    <div class="portal-kicker">Municipal Governance • Data & Insights</div>
    <div class="portal-title">Civic Analytics & Decision Support</div>
    <p class="portal-subtitle">
        Evidence-based insights into civic complaints,
        service delivery and resolution performance.
    </p>
    <div class="portal-tagline">
        Intelligence for Better Governance. Transparency for Better Cities.
    </div>
</div>
""")

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

DATA_FILE = Path(__file__).resolve().parent.parent / "bmc_train.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, low_memory=False)

    for col in [
        "citizen_satisfied",
        "resolution_days",
        "year",
        "month",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Dataset not found. Please ensure bmc_train.csv "
        "is available in the main project folder."
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

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing required dataset columns: {missing}")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.markdown("## CIVIC ANALYTICS")
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Filters")
st.sidebar.caption("Refine the historical complaint records.")

filtered_df = df.copy()

years = sorted(
    filtered_df["year"].dropna().unique().tolist()
)

if years:
    selected_years = st.sidebar.multiselect(
        "Reporting Year",
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
        "Municipal Zone",
        options=zones,
        default=zones,
    )

    if selected_zones:
        filtered_df = filtered_df[
            filtered_df["zone"].astype(str).isin(selected_zones)
        ]
    else:
        filtered_df = filtered_df.iloc[0:0]


st.sidebar.markdown("---")
st.sidebar.caption("Data source: Mumbai civic complaint dataset, 2018–2024.")
st.sidebar.caption("Educational prototype • Not a live municipal database.")


if filtered_df.empty:
    st.warning(
        "No records match the selected filters. "
        "Please select at least one year and one zone."
    )
    st.stop()


# --------------------------------------------------
# HELPER: KPI CARD
# --------------------------------------------------

def kpi_card(label, value, note="Historical dataset"):
    st.html(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """)


def section_heading(title, description):
    st.markdown(
        f'<div class="section-heading">{title}</div>'
        f'<div class="section-description">{description}</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

section_heading(
    "01 | Civic Performance Overview",
    "A consolidated view of complaint volume, citizen satisfaction "
    "and resolution performance."
)

total_complaints = len(filtered_df)

satisfaction = filtered_df["citizen_satisfied"].dropna()

if len(satisfaction) > 0:
    satisfaction_rate = satisfaction.eq(1).mean() * 100
else:
    satisfaction_rate = None

resolution = filtered_df["resolution_days"].dropna()

if len(resolution) > 0:
    average_resolution = resolution.mean()
else:
    average_resolution = None


c1, c2, c3 = st.columns(3)

with c1:
    kpi_card(
        "Total Complaints",
        f"{total_complaints:,}",
        "Records matching current filters"
    )

with c2:
    kpi_card(
        "Citizen Satisfaction",
        f"{satisfaction_rate:.1f}%" if satisfaction_rate is not None else "N/A",
        "Share of records marked satisfied"
    )

with c3:
    kpi_card(
        "Average Resolution",
        f"{average_resolution:.1f} days" if average_resolution is not None else "N/A",
        "Mean recorded resolution time"
    )


st.html("""
<div class="info-panel">
    <b>Data interpretation:</b> These indicators describe historical
    dataset records. They are not live service statistics or future predictions.
</div>
""")


# --------------------------------------------------
# CHART 1: COMPLAINT CATEGORIES
# --------------------------------------------------

st.divider()

section_heading(
    "02 | Complaint Category Analysis",
    "Identify the most frequently recorded civic complaint categories."
)

category_counts = (
    filtered_df["complaint_category"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
    .rename_axis("Complaint Category")
    .reset_index(name="Number of Complaints")
    .sort_values("Number of Complaints")
)

category_chart = (
    alt.Chart(category_counts)
    .mark_bar(cornerRadiusEnd=5, color="#263C50")
    .encode(
        x=alt.X(
            "Number of Complaints:Q",
            title="Number of Complaints",
            axis=alt.Axis(format=",")
        ),
        y=alt.Y(
            "Complaint Category:N",
            sort=None,
            title="Complaint Category",
            axis=alt.Axis(labelLimit=260)
        ),
        tooltip=[
            "Complaint Category",
            alt.Tooltip("Number of Complaints:Q", format=",")
        ]
    )
    .properties(height=360)
)

st.altair_chart(category_chart, use_container_width=True)


# --------------------------------------------------
# CHART 2: COMPLAINT TRENDS
# --------------------------------------------------

st.divider()

section_heading(
    "03 | Complaint Trends Over Time",
    "Explore how recorded complaint volumes change across months and years."
)

monthly = filtered_df.dropna(
    subset=["year", "month"]
).copy()

monthly["year"] = monthly["year"].astype(int)
monthly["month"] = monthly["month"].astype(int)

monthly = monthly[monthly["month"].between(1, 12)]

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
    trend_df = trend.reset_index()
    trend_df.columns = ["Period", "Complaints"]

    trend_chart = (
        alt.Chart(trend_df)
        .mark_line(
            color="#263C50",
            strokeWidth=3,
            point=alt.OverlayMarkDef(
                filled=True,
                color="#C5A15B",
                size=45
            )
        )
        .encode(
            x=alt.X("Period:N", title="Reporting Month", sort=None),
            y=alt.Y(
                "Complaints:Q",
                title="Number of Complaints",
                axis=alt.Axis(format=",")
            ),
            tooltip=["Period", alt.Tooltip("Complaints:Q", format=",")]
        )
        .properties(height=320)
    )

    st.altair_chart(trend_chart, use_container_width=True)

else:
    st.info("No valid year/month records are available for this chart.")


# --------------------------------------------------
# CHART 3: SATISFACTION BY ZONE
# --------------------------------------------------

st.divider()

section_heading(
    "04 | Citizen Satisfaction by Zone",
    "Compare the percentage of complaints marked satisfied across zones."
)

zone_data = filtered_df.dropna(
    subset=["zone", "citizen_satisfied"]
).copy()

if not zone_data.empty:

    zone_rates = (
        zone_data.groupby("zone")["citizen_satisfied"]
        .apply(lambda values: values.eq(1).mean() * 100)
        .sort_values(ascending=False)
        .reset_index(name="Satisfaction Rate")
    )

    satisfaction_chart = (
        alt.Chart(zone_rates)
        .mark_bar(cornerRadiusEnd=5, color="#C5A15B")
        .encode(
            x=alt.X(
                "Satisfaction Rate:Q",
                title="Satisfaction Rate (%)",
                scale=alt.Scale(domain=[0, 100])
            ),
            y=alt.Y(
                "zone:N",
                sort="-x",
                title="Municipal Zone"
            ),
            tooltip=[
                "zone",
                alt.Tooltip("Satisfaction Rate:Q", format=".1f")
            ]
        )
        .properties(height=300)
    )

    st.altair_chart(satisfaction_chart, use_container_width=True)

else:
    st.info("No satisfaction data is available for the selected filters.")


# --------------------------------------------------
# CHART 4: RESOLUTION TIME
# --------------------------------------------------

st.divider()

section_heading(
    "05 | Complaint Resolution Performance",
    "Understand the distribution of recorded complaint resolution times."
)

valid_resolution = resolution[resolution >= 0]

if not valid_resolution.empty:

    median_days = valid_resolution.median()
    percentile_95 = valid_resolution.quantile(0.95)

    c1, c2 = st.columns(2)

    c1.metric("Median Resolution Time", f"{median_days:.1f} days")
    c2.metric("95th Percentile", f"{percentile_95:.1f} days")

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

    resolution_chart = (
        alt.Chart(histogram)
        .mark_bar(color="#263C50")
        .encode(
            x=alt.X(
                "Resolution Time Range:N",
                title="Resolution Time Range",
                axis=alt.Axis(labelAngle=-45)
            ),
            y=alt.Y(
                "Number of Complaints:Q",
                title="Number of Complaints"
            ),
            tooltip=["Resolution Time Range", "Number of Complaints"]
        )
        .properties(height=320)
    )

    st.altair_chart(resolution_chart, use_container_width=True)

    st.caption(
        "For display, records above the 95th percentile are excluded "
        "from this distribution chart. They remain in the dataset."
    )

else:
    st.info("No valid resolution-time records are available.")


# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.divider()

section_heading(
    "06 | Historical Data Explorer",
    "Inspect a sample of the records matching your selected filters."
)

with st.expander("Open filtered dataset preview"):

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

    st.caption(
        f"Showing up to 100 of {len(filtered_df):,} filtered records."
    )


# --------------------------------------------------
# ESCALATION ANALYSIS
# --------------------------------------------------

st.divider()

section_heading(
    "07 | Complaint Escalation Monitoring",
    "Examine historical escalation patterns across complaint categories, "
    "municipal zones, severity levels and recorded statuses."
)

if "complaint_status" not in filtered_df.columns:
    st.warning(
        "The complaint_status column is unavailable. "
        "Escalation analysis cannot be displayed."
    )

else:

    escalated_df = filtered_df[
        filtered_df["complaint_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("escalated")
    ].copy()

    total_escalated = len(escalated_df)

    escalation_rate = (
        total_escalated / total_complaints * 100
        if total_complaints > 0
        else 0
    )

    non_escalated = total_complaints - total_escalated

    e1, e2, e3 = st.columns(3)

    with e1:
        kpi_card(
            "Escalated Complaints",
            f"{total_escalated:,}",
            "Recorded as escalated"
        )

    with e2:
        kpi_card(
            "Escalation Percentage",
            f"{escalation_rate:.2f}%",
            "Share of filtered complaints"
        )

    with e3:
        kpi_card(
            "Non-Escalated Complaints",
            f"{non_escalated:,}",
            "All other recorded statuses"
        )

    st.caption(
        "Escalation percentage = escalated complaints / "
        "total filtered complaints × 100."
    )

    # ----------------------------------------------
    # ESCALATIONS BY CATEGORY
    # ----------------------------------------------

    st.markdown("#### 7.1 Escalated Complaints by Category")

    if not escalated_df.empty:

        category_escalations = (
            escalated_df["complaint_category"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .rename_axis("Complaint Category")
            .reset_index(name="Escalated Complaints")
            .sort_values("Escalated Complaints")
        )

        category_escalation_chart = (
            alt.Chart(category_escalations)
            .mark_bar(cornerRadiusEnd=5, color="#263C50")
            .encode(
                x=alt.X(
                    "Escalated Complaints:Q",
                    title="Number of Escalated Complaints"
                ),
                y=alt.Y(
                    "Complaint Category:N",
                    sort=None,
                    title="Complaint Category",
                    axis=alt.Axis(labelLimit=260)
                ),
                tooltip=[
                    "Complaint Category",
                    "Escalated Complaints"
                ]
            )
            .properties(height=340)
        )

        st.altair_chart(
            category_escalation_chart,
            use_container_width=True
        )

    else:
        st.info("No escalated complaints match the selected filters.")

    # ----------------------------------------------
    # ESCALATIONS BY ZONE
    # ----------------------------------------------

    st.markdown("#### 7.2 Escalated Complaints by Zone")

    if not escalated_df.empty:

        zone_escalations = (
            escalated_df["zone"]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("Zone")
            .reset_index(name="Escalated Complaints")
        )

        zone_escalation_chart = (
            alt.Chart(zone_escalations)
            .mark_bar(cornerRadiusEnd=5, color="#C5A15B")
            .encode(
                x=alt.X(
                    "Escalated Complaints:Q",
                    title="Number of Escalated Complaints"
                ),
                y=alt.Y(
                    "Zone:N",
                    sort="-x",
                    title="Municipal Zone"
                ),
                tooltip=["Zone", "Escalated Complaints"]
            )
            .properties(height=300)
        )

        st.altair_chart(
            zone_escalation_chart,
            use_container_width=True
        )

    else:
        st.info("No zone-wise escalation data is available.")

    # ----------------------------------------------
    # ESCALATION BY SEVERITY
    # ----------------------------------------------

    st.markdown("#### 7.3 Escalation Percentage by Severity")

    if "severity" in filtered_df.columns:

        severity_data = filtered_df.dropna(
            subset=["severity", "complaint_status"]
        ).copy()

        if not severity_data.empty:

            severity_data["Is Escalated"] = (
                severity_data["complaint_status"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("escalated")
            )

            severity_rates = (
                severity_data.groupby("severity")["Is Escalated"]
                .mean()
                .mul(100)
                .sort_values(ascending=False)
                .rename("Escalation Percentage")
                .reset_index()
            )

            severity_chart = (
                alt.Chart(severity_rates)
                .mark_bar(cornerRadiusEnd=5, color="#263C50")
                .encode(
                    x=alt.X(
                        "Escalation Percentage:Q",
                        title="Escalation Percentage (%)"
                    ),
                    y=alt.Y(
                        "severity:N",
                        sort="-x",
                        title="Severity Level"
                    ),
                    tooltip=[
                        "severity",
                        alt.Tooltip(
                            "Escalation Percentage:Q",
                            format=".2f"
                        )
                    ]
                )
                .properties(height=280)
            )

            st.altair_chart(
                severity_chart,
                use_container_width=True
            )

            st.caption(
                "Percentage of complaints escalated within each severity category."
            )

        else:
            st.info("No severity data is available.")

    else:
        st.info("Severity column is unavailable.")

    # ----------------------------------------------
    # COMPLAINT STATUS DISTRIBUTION
    # ----------------------------------------------

    st.markdown("#### 7.4 Complaint Status Distribution")

    status_counts = (
        filtered_df["complaint_status"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Complaint Status")
        .reset_index(name="Number of Complaints")
    )

    if not status_counts.empty:

        status_chart = (
            alt.Chart(status_counts)
            .mark_bar(cornerRadiusEnd=5, color="#C5A15B")
            .encode(
                x=alt.X(
                    "Number of Complaints:Q",
                    title="Number of Complaints"
                ),
                y=alt.Y(
                    "Complaint Status:N",
                    sort="-x",
                    title="Complaint Status"
                ),
                tooltip=[
                    "Complaint Status",
                    "Number of Complaints"
                ]
            )
            .properties(height=300)
        )

        st.altair_chart(
            status_chart,
            use_container_width=True
        )

    with st.expander("View complaint status counts"):
        st.dataframe(
            status_counts,
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.html("""
<div class="footer-panel">
    <b>SMART CIVIC COMPLAINT INTELLIGENCE</b><br>
    Intelligence for Better Governance. Transparency for Better Cities.<br><br>
    Educational prototype • Historical dataset analysis •
    Not an official BMC service
</div>
""")
