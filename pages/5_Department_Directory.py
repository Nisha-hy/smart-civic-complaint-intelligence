
import streamlit as st


# ==================================================
# 1. GOVERNMENT PORTAL DESIGN SYSTEM
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

.department-card {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-top: 4px solid #C5A15B;
    border-radius: 10px;
    padding: 22px;
    margin: 12px 0;
}

.department-label {
    color: #647181;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.department-name {
    color: #101B2D;
    font-size: 22px;
    font-weight: 750;
    margin-top: 10px;
}

.contact-card {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-top: 4px solid #C5A15B;
    border-radius: 10px;
    padding: 20px;
    min-height: 125px;
}

.contact-label {
    color: #647181;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

.contact-value {
    color: #101B2D;
    font-size: 27px;
    font-weight: 750;
    margin-top: 10px;
}

.stButton button {
    background-color: #101B2D;
    color: #FFFFFF;
    border: 1px solid #C5A15B;
    border-radius: 7px;
}

.stButton button:hover {
    background-color: #263C50;
    color: #FFFFFF;
    border-color: #C5A15B;
}

div[data-testid="stSelectbox"] label {
    color: #263C50;
    font-weight: 650;
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
# 2. PORTAL HEADER
# ==================================================

st.html("""
<div class="portal-banner">

    <div class="portal-kicker">
        Municipal Governance • Public Services
    </div>

    <div class="portal-title">
        Municipal Department Directory
    </div>

    <div class="portal-subtitle">
        Identify the suggested municipal department for common
        civic concerns and find official BMC contact channels.
    </div>

    <div class="portal-tagline">
        Intelligence for Better Governance.
        Transparency for Better Cities.
    </div>

</div>
""")

st.html("""
<div class="info-panel">
    <b>Department Information Service</b><br>
    Find an indicative department for your selected complaint
    category and explore official BMC contact channels.
    <br><br>
    This directory is an informational guide. It does not
    automatically forward complaints to BMC or determine
    official complaint routing.
</div>
""")


# ==================================================
# 3. COMPLAINT-TO-DEPARTMENT DIRECTORY
# ==================================================

departments = {

    "Pothole / Road Damage":
        "Roads and Bridges Department",

    "Damaged Footpath":
        "Roads and Bridges Department",

    "Garbage / Waste Collection":
        "Solid Waste Management Department",

    "Overflowing Garbage Bin":
        "Solid Waste Management Department",

    "Water Leakage":
        "Water Works Department",

    "No Water Supply":
        "Water Supply Department",

    "Blocked Rainwater Drain":
        "Storm Water Drains Department",

    "Sewage Overflow":
        "Sewerage Operations Department",

    "Streetlight Problem":
        "Mechanical and Electrical Department",

    "Mosquito / Pest Problem":
        "Public Health Department - Insecticide Branch",

    "Public Health / Sanitation Issue":
        "Public Health Department",

    "Illegal Building / Construction":
        "Building and Factory Department",

    "Building Approval Issue":
        "Building Proposal Department",

    "Roadside Encroachment":
        "Encroachment Department",

    "Tree Cutting / Fallen Branch":
        "Garden and Tree Department",

    "Unauthorised Shop / Licence Issue":
        "Licence Department",

    "Shop and Establishment Issue":
        "Shops and Establishments Department",

    "Property Tax Issue":
        "Assessment and Collection Department",

    "Public Market Issue":
        "Market Department",

    "School Infrastructure Issue":
        "Education Department",

    "Fire Safety Concern":
        "Mumbai Fire Brigade",

    "Other":
        "BMC Central Complaint Registration",
}


# ==================================================
# 4. FIND THE RELEVANT DEPARTMENT
# ==================================================

st.markdown(
    '<div class="section-heading">01 | Find the Relevant Department</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select your civic complaint category to identify the suggested '
    'municipal department.'
    '</div>',
    unsafe_allow_html=True
)

category = st.selectbox(
    "Select Your Complaint Category",
    list(departments.keys())
)

suggested_department = departments[category]

st.html(f"""
<div class="department-card">

    <div class="department-label">
        Suggested Municipal Department
    </div>

    <div class="department-name">
        {suggested_department}
    </div>

    <div style="
        color: #647181;
        font-size: 13px;
        margin-top: 12px;
    ">
        Selected complaint category: {category}
    </div>

</div>
""")

st.caption(
    "The suggested department is indicative. "
    "Official BMC authorities determine the actual complaint routing."
)


# ==================================================
# 5. OFFICIAL BMC CONTACT CHANNELS
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">02 | Official BMC Contact Channels</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Use the following official channels to seek municipal assistance.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.html("""
    <div class="contact-card">

        <div class="contact-label">
            Civic Complaint Helpline
        </div>

        <div class="contact-value">
            1916
        </div>

        <div style="
            color: #647181;
            font-size: 12px;
            margin-top: 5px;
        ">
            BMC civic complaint helpline
        </div>

    </div>
    """)

with col2:

    st.html(f"""
    <div class="contact-card">

        <div class="contact-label">
            Complaint Categories
        </div>

        <div class="contact-value">
            {len(departments)}
        </div>

        <div style="
            color: #647181;
            font-size: 12px;
            margin-top: 5px;
        ">
            Categories covered in this directory
        </div>

    </div>
    """)


st.markdown("#### Official Online Resources")

st.markdown(
    "[Visit Official BMC Website](https://www.mcgm.gov.in/)"
)

st.markdown(
    "[Official BMC Complaint Information](https://www.mcgm.gov.in/irj/portal/anonymous?NavigationTarget=navurl%3A%2F%2F1541a2917b15d1b4a1a0713c12eb56ff&guest_user=english)"
)


# ==================================================
# 6. HOW TO CONTACT BMC
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">03 | How to Contact BMC</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A simple guide for citizens seeking assistance with civic concerns.'
    '</div>',
    unsafe_allow_html=True
)

steps = [
    (
        "01",
        "Select Your Complaint Category",
        "Choose the category that best describes your civic concern."
    ),
    (
        "02",
        "Identify the Suggested Department",
        "Review the indicative municipal department shown in the directory."
    ),
    (
        "03",
        "Contact BMC",
        "Use the civic complaint helpline 1916 for assistance."
    ),
    (
        "04",
        "Use Official Complaint Facilities",
        "Visit the official BMC website for available complaint services."
    ),
]

for number, title, description in steps:

    with st.container(border=True):

        col1, col2 = st.columns([1, 8])

        with col1:

            st.markdown(
                f"### <span style='color:#C5A15B'>{number}</span>",
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(f"**{title}**")

            st.caption(description)


# ==================================================
# 7. IMPORTANT SERVICE INFORMATION
# ==================================================

st.divider()

st.warning(
    "For urgent fire or safety emergencies, contact the appropriate "
    "emergency service directly. This directory is not an "
    "emergency-response service."
)

st.info(
    "Your Smart Civic Complaint reference ID is generated by this "
    "local prototype. It is not an official BMC complaint ID."
)


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

    Public Information • Academic Demonstration Prototype
    <br>
    Not an Official BMC Service

</div>
""")
