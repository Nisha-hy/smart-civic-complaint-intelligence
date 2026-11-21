
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st


# ==================================================
# 1. DATABASE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "civic_complaints.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ==================================================
# 2. GOVERNMENT PORTAL DESIGN SYSTEM
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F2EA;
    color: #101B2D;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background-color: #101B2D;
}

[data-testid="stSidebar"] * {
    color: #F5F2EA;
}

h1, h2, h3, h4 {
    color: #101B2D;
}

.portal-banner {
    background: linear-gradient(110deg, #101B2D, #263C50);
    border-bottom: 5px solid #C5A15B;
    padding: 28px 32px;
    border-radius: 12px;
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
    margin: 10px 0 7px 0;
}

.portal-subtitle {
    color: #E3E8ED;
    font-size: 14px;
}

.portal-tagline {
    color: #D8BD83;
    font-size: 13px;
    font-style: italic;
    margin-top: 16px;
}

.section-heading {
    color: #101B2D;
    font-size: 21px;
    font-weight: 750;
    border-left: 5px solid #C5A15B;
    padding-left: 13px;
    margin-top: 15px;
    margin-bottom: 7px;
}

.section-description {
    color: #647181;
    font-size: 13px;
    margin-bottom: 17px;
}

.info-panel {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-left: 5px solid #C5A15B;
    border-radius: 8px;
    padding: 15px 19px;
    margin: 12px 0 22px 0;
    color: #526071;
    font-size: 13px;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-top: 4px solid #C5A15B;
    border-radius: 10px;
    padding: 18px;
    min-height: 112px;
}

.kpi-label {
    color: #647181;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.kpi-value {
    color: #101B2D;
    font-size: 27px;
    font-weight: 750;
    margin-top: 10px;
}

.kpi-note {
    color: #87909A;
    font-size: 11px;
    margin-top: 4px;
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 10px;
    padding: 22px;
}

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextArea"] label {
    color: #263C50;
    font-weight: 650;
}

.stButton button,
.stFormSubmitButton button {
    background-color: #101B2D;
    color: #FFFFFF;
    border: 1px solid #C5A15B;
    border-radius: 7px;
    min-height: 43px;
    font-weight: 650;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #263C50;
    color: #FFFFFF;
    border-color: #C5A15B;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-top: 4px solid #C5A15B;
    border-radius: 9px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #647181;
}

div[data-testid="stMetricValue"] {
    color: #101B2D;
}

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 8px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E5E0D5;
    border-radius: 8px;
}

.footer-panel {
    background: #101B2D;
    color: #DDE3E9;
    padding: 19px;
    border-radius: 9px;
    text-align: center;
    font-size: 12px;
    margin-top: 28px;
}

hr {
    border-color: #DED9CB;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. PORTAL HEADER
# ==================================================

st.html("""
<div class="portal-banner">

    <div class="portal-kicker">
        Municipal Governance • Administration
    </div>

    <div class="portal-title">
        Municipal Administrator Portal
    </div>

    <div class="portal-subtitle">
        Monitor registered civic complaints, review service requests
        and maintain their recorded progress.
    </div>

    <div class="portal-tagline">
        Intelligence for Better Governance.
        Transparency for Better Cities.
    </div>

</div>
""")

st.html("""
<div class="info-panel">
    <b>Administrative Demonstration Workspace</b><br>
    Review complaint records and update their status using this
    local prototype.
    <br><br>
    <b>Prototype notice:</b> Updates are stored in the local
    application database. They do not update BMC records.
    This demonstration portal does not include administrator
    authentication.
</div>
""")


# ==================================================
# 4. LOAD REGISTERED COMPLAINTS
# ==================================================

try:

    with get_connection() as connection:

        complaints = pd.read_sql_query(
            """
            SELECT
                reference_id,
                submitted_at,
                citizen_name,
                ward_area,
                category,
                severity,
                description,
                status
            FROM complaints
            ORDER BY id DESC
            """,
            connection,
        )

except Exception as error:

    st.error(f"Could not load complaint records: {error}")
    st.stop()


# ==================================================
# 5. COMPLAINT OVERVIEW
# ==================================================

st.markdown(
    '<div class="section-heading">01 | Complaint Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A consolidated summary of complaints registered in this prototype.'
    '</div>',
    unsafe_allow_html=True
)

total_complaints = len(complaints)

if total_complaints > 0:

    submitted_count = (
        complaints["status"] == "Submitted"
    ).sum()

    progress_count = (
        complaints["status"] == "In Progress"
    ).sum()

    resolved_count = (
        complaints["status"] == "Resolved"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "Total Complaints", total_complaints),
        (col2, "Submitted", submitted_count),
        (col3, "In Progress", progress_count),
        (col4, "Resolved", resolved_count),
    ]

    for column, label, value in metrics:

        with column:

            st.html(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{int(value):,}</div>
                <div class="kpi-note">Local prototype records</div>
            </div>
            """)

else:

    st.info("No complaints have been registered yet.")


# ==================================================
# 6. REGISTERED COMPLAINTS
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">02 | Registered Complaints</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Review complaint details and search using a reference ID.'
    '</div>',
    unsafe_allow_html=True
)

if total_complaints > 0:

    st.dataframe(
        complaints,
        use_container_width=True,
        hide_index=True
    )

    search_id = st.text_input(
        "Search by Complaint Reference ID",
        placeholder="Example: SCI-2026-00001",
        key="admin_search_id"
    )

    if search_id.strip():

        filtered = complaints[
            complaints["reference_id"]
            .fillna("")
            .astype(str)
            .str.upper()
            == search_id.strip().upper()
        ]

        if not filtered.empty:

            st.success("Matching complaint found.")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No matching complaint found.")

else:

    st.info("Complaint records will appear here after registration.")


# ==================================================
# 7. UPDATE COMPLAINT STATUS
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">03 | Update Complaint Status</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select a registered complaint and record its latest status.'
    '</div>',
    unsafe_allow_html=True
)

if total_complaints > 0:

    reference_ids = complaints["reference_id"].dropna().tolist()

    if reference_ids:

        selected_reference = st.selectbox(
            "Select Complaint Reference ID",
            reference_ids,
            key="admin_update_reference"
        )

        selected_complaint = complaints[
            complaints["reference_id"] == selected_reference
        ].iloc[0]

        with st.container(border=True):

            st.markdown("#### Selected Complaint Details")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("**Complaint Category**")
                st.write(selected_complaint["category"])

                st.markdown("**Ward Area**")
                st.write(selected_complaint["ward_area"])

            with col2:

                st.markdown("**Severity**")
                st.write(selected_complaint["severity"])

                st.markdown("**Current Status**")
                st.write(selected_complaint["status"])

        status_options = [
            "Submitted",
            "Under Review",
            "Assigned to Department",
            "In Progress",
            "Resolved",
            "Closed Without Resolution",
        ]

        current_status = selected_complaint["status"]

        status_index = (
            status_options.index(current_status)
            if current_status in status_options
            else 0
        )

        new_status = st.selectbox(
            "Select New Status",
            status_options,
            index=status_index,
            key="admin_new_status"
        )

        remarks = st.text_area(
            "Administrator Remarks",
            placeholder="Enter details about this status update...",
            height=110,
            key="admin_remarks"
        )

        if st.button(
            "Update Complaint Status",
            type="primary",
            use_container_width=True
        ):

            if new_status == current_status:

                st.warning("Please select a different status.")

            elif not remarks.strip():

                st.error("Please enter remarks for the update.")

            else:

                updated_at = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                try:

                    with get_connection() as connection:

                        connection.execute(
                            """
                            UPDATE complaints
                            SET status = ?
                            WHERE reference_id = ?
                            """,
                            (new_status, selected_reference),
                        )

                        connection.execute(
                            """
                            INSERT INTO status_history (
                                reference_id,
                                status,
                                updated_at,
                                remarks
                            )
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                selected_reference,
                                new_status,
                                updated_at,
                                remarks.strip(),
                            ),
                        )

                    st.success(
                        f"Complaint {selected_reference} updated successfully!"
                    )

                    st.rerun()

                except Exception as error:

                    st.error(f"Could not update complaint: {error}")

    else:

        st.info("No valid complaint reference IDs are available.")

else:

    st.info("Register a complaint through the Citizen Portal first.")


# ==================================================
# 8. COMPLAINT UPDATE HISTORY
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">04 | Complaint Update History</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Review the recorded status changes and administrator remarks.'
    '</div>',
    unsafe_allow_html=True
)

if total_complaints > 0:

    history_references = complaints["reference_id"].dropna().tolist()

    if history_references:

        history_reference = st.selectbox(
            "Select Complaint to View History",
            history_references,
            key="history_reference"
        )

        try:

            with get_connection() as connection:

                history = pd.read_sql_query(
                    """
                    SELECT status, updated_at, remarks
                    FROM status_history
                    WHERE reference_id = ?
                    ORDER BY id ASC
                    """,
                    connection,
                    params=(history_reference,),
                )

            if not history.empty:

                for index, record in history.iterrows():

                    with st.container(border=True):

                        st.markdown(
                            f"**{index + 1:02d} | {record['status']}**"
                        )

                        st.caption(record["updated_at"])

                        st.write(record["remarks"])

            else:

                st.info("No status updates found.")

        except Exception as error:

            st.error(f"Could not retrieve update history: {error}")

else:

    st.info("No complaint history is available yet.")


# ==================================================
# 9. PORTAL FOOTER
# ==================================================

st.html("""
<div class="footer-panel">

    <b>SMART CIVIC COMPLAINT INTELLIGENCE</b>

    <br><br>

    Intelligence for Better Governance.
    Transparency for Better Cities.

    <br><br>

    Administrative Workspace • Academic Demonstration Prototype
    <br>
    Not an Official BMC Service

</div>
""")
