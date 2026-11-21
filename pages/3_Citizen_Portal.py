
import sqlite3
from pathlib import Path
from datetime import datetime

import streamlit as st


# ==================================================
# 1. DATABASE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "civic_complaints.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference_id TEXT UNIQUE,
                submitted_at TEXT,
                citizen_name TEXT,
                ward_area TEXT,
                category TEXT,
                severity TEXT,
                description TEXT,
                status TEXT DEFAULT 'Submitted'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS status_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference_id TEXT,
                status TEXT,
                updated_at TEXT,
                remarks TEXT
            )
        """)


initialize_database()


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

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 10px;
    padding: 22px;
}

div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
div[data-testid="stTextArea"] {
    color: #101B2D;
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
        Municipal Governance • Citizen Services
    </div>

    <div class="portal-title">
        Citizen Complaint Portal
    </div>

    <div class="portal-subtitle">
        Register civic concerns and follow the recorded progress
        of your complaint through this demonstration portal.
    </div>

    <div class="portal-tagline">
        Intelligence for Better Governance.
        Transparency for Better Cities.
    </div>

</div>
""")

st.html("""
<div class="info-panel">
    <b>Citizen Service Information</b><br>
    Use this portal to register a civic complaint, receive a
    reference ID and check its recorded status.
    <br><br>
    <b>Prototype notice:</b> Complaints are stored in this
    application's local database. They are not submitted to
    the official BMC system.
</div>
""")


# ==================================================
# 4. COMPLAINT FORM OPTIONS
# ==================================================

categories = [
    "Water Leakage / Pipe Burst",
    "Public Toilet Condition",
    "Tree Fallen / Dangerous Tree",
    "Encroachment",
    "Illegal Construction",
    "Street Light Failure",
    "Drainage Overflow / Flooding",
    "Solid Waste / Garbage",
    "Water Supply Disruption",
    "Pothole / Road Damage",
    "Other",
]

ward_areas = [
    "Andheri East",
    "Andheri West",
    "Bandra",
    "Borivali",
    "Dadar",
    "Kurla",
    "Other",
]


# ==================================================
# 5. REGISTER A NEW COMPLAINT
# ==================================================

st.markdown(
    '<div class="section-heading">01 | Register a Complaint</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Provide the relevant information about the civic issue.'
    '</div>',
    unsafe_allow_html=True
)


with st.form("citizen_complaint_form", clear_on_submit=True):

    st.markdown("#### Complaint Details")

    citizen_name = st.text_input(
        "Citizen Name (Optional)",
        placeholder="Enter your name"
    )

    col1, col2 = st.columns(2)

    with col1:
        ward_area = st.selectbox(
            "Ward Area",
            ward_areas
        )

    with col2:
        category = st.selectbox(
            "Complaint Category",
            categories
        )

    severity = st.selectbox(
        "Complaint Severity",
        ["Low", "Medium", "High", "Critical"]
    )

    description = st.text_area(
        "Describe Your Complaint",
        placeholder=(
            "Explain the civic issue and mention its "
            "location or other useful details..."
        ),
        height=130
    )

    submit_complaint = st.form_submit_button(
        "Submit Complaint",
        type="primary",
        use_container_width=True
    )


if submit_complaint:

    if not description.strip():

        st.error("Please enter a complaint description.")

    else:

        submitted_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:

            with get_connection() as connection:

                cursor = connection.execute(
                    """
                    INSERT INTO complaints (
                        submitted_at,
                        citizen_name,
                        ward_area,
                        category,
                        severity,
                        description,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        submitted_at,
                        citizen_name.strip(),
                        ward_area,
                        category,
                        severity,
                        description.strip(),
                        "Submitted",
                    ),
                )

                complaint_number = cursor.lastrowid

                reference_id = (
                    f"SCI-{datetime.now().year}-{complaint_number:05d}"
                )

                connection.execute(
                    """
                    UPDATE complaints
                    SET reference_id = ?
                    WHERE id = ?
                    """,
                    (reference_id, complaint_number),
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
                        reference_id,
                        "Submitted",
                        submitted_at,
                        "Complaint registered in the prototype.",
                    ),
                )

            st.session_state["last_submitted_reference"] = reference_id

        except Exception as error:

            st.error(f"Could not register the complaint: {error}")


# Display the most recently generated reference ID.

if st.session_state.get("last_submitted_reference"):

    st.success("Complaint registered successfully!")

    st.markdown("#### Your Complaint Reference ID")

    st.code(
        st.session_state["last_submitted_reference"],
        language=None
    )

    st.warning(
        "Save this reference ID. You will need it to track "
        "your complaint."
    )


# ==================================================
# 6. TRACK A REGISTERED COMPLAINT
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">02 | Track Your Complaint</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter your complaint reference ID to view its current '
    'recorded status and update history.'
    '</div>',
    unsafe_allow_html=True
)


reference_input = st.text_input(
    "Complaint Reference ID",
    placeholder="Example: SCI-2026-00001",
    key="tracking_reference_input"
)


if st.button(
    "Track Complaint",
    type="primary",
    use_container_width=True
):

    reference_id = reference_input.strip().upper()

    if not reference_id:

        st.error("Please enter a complaint reference ID.")

        st.session_state.pop("tracked_complaint", None)

    else:

        try:

            with get_connection() as connection:

                complaint = connection.execute(
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
                    WHERE reference_id = ?
                    """,
                    (reference_id,),
                ).fetchone()

                history = connection.execute(
                    """
                    SELECT status, updated_at, remarks
                    FROM status_history
                    WHERE reference_id = ?
                    ORDER BY id ASC
                    """,
                    (reference_id,),
                ).fetchall()

            if complaint:

                st.session_state["tracked_complaint"] = {
                    "complaint": complaint,
                    "history": history,
                }

            else:

                st.session_state.pop("tracked_complaint", None)
                st.error("No complaint found with this reference ID.")

        except Exception as error:

            st.error(f"Could not retrieve complaint details: {error}")


# ==================================================
# 7. DISPLAY COMPLAINT DETAILS
# ==================================================

tracked_data = st.session_state.get("tracked_complaint")

if tracked_data:

    complaint = tracked_data["complaint"]
    history = tracked_data["history"]

    (
        ref_id,
        submitted_at,
        name,
        area,
        complaint_category,
        complaint_severity,
        complaint_description,
        status,
    ) = complaint

    st.success("Complaint record found!")

    st.markdown("#### Complaint Status")

    st.metric(
        "Current Complaint Status",
        status
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Reference ID**")
        st.code(ref_id, language=None)

        st.markdown("**Submitted At**")
        st.write(submitted_at)

        st.markdown("**Ward Area**")
        st.write(area)

        st.markdown("**Complaint Category**")
        st.write(complaint_category)

    with col2:

        st.markdown("**Citizen Name**")
        st.write(name if name else "Not provided")

        st.markdown("**Complaint Severity**")
        st.write(complaint_severity)

    st.markdown("**Complaint Description**")

    with st.container(border=True):
        st.write(complaint_description)

    st.markdown("#### Complaint Status History")

    if history:

        for index, item in enumerate(history, start=1):

            history_status, updated_at, remarks = item

            with st.container(border=True):

                st.markdown(
                    f"**{index:02d} | {history_status}**"
                )

                st.caption(updated_at)

                st.write(remarks)

    else:

        st.info("No status updates have been recorded yet.")


# ==================================================
# 8. PORTAL FOOTER
# ==================================================

st.html("""
<div class="footer-panel">

    <b>SMART CIVIC COMPLAINT INTELLIGENCE</b>

    <br><br>

    Intelligence for Better Governance.
    Transparency for Better Cities.

    <br><br>

    Citizen Services • Academic Demonstration Prototype
    <br>
    Not an Official BMC Service

</div>
""")
