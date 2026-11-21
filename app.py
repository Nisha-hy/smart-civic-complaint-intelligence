
import streamlit as st

st.set_page_config(
    page_title="Smart Civic Complaint Intelligence",
    page_icon="🏙️",
    layout="wide"
)

prediction_page = st.Page(
    "pages/1_Predictions.py",
    title="ML Predictions",
    icon="🧠",
    default=True
)

analytics_page = st.Page(
    "pages/2_Civic_Analytics.py",
    title="Civic Analytics",
    icon="📊"
)

citizen_page = st.Page(
    "pages/3_Citizen_Portal.py",
    title="Citizen Portal",
    icon="👥"
)

admin_page = st.Page(
    "pages/4_Admin_Portal.py",
    title="Administrator Portal",
    icon="🛡️"
)

department_page = st.Page(
    "pages/5_Department_Directory.py",
    title="Department Directory",
    icon="🏢"
)

pg = st.navigation([
    prediction_page,
    analytics_page,
    citizen_page,
    admin_page,
    department_page
])

pg.run()
