
import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SATISFACTION_MODEL = BASE_DIR / "civic_satisfaction_model.joblib"
ESCALATION_MODEL = BASE_DIR / "civic_escalation_model.joblib"


# ==================================================
# 2. GOVERNMENT PORTAL DESIGN SYSTEM
# ==================================================

st.markdown("""
<style>

/* Application background */
.stApp {
    background-color: #F5F2EA;
    color: #101B2D;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #101B2D;
}

section[data-testid="stSidebar"] * {
    color: #F5F2EA;
}

/* Main headings */
h1, h2, h3, h4 {
    color: #101B2D;
}

/* Section heading */
.section-title {
    color: #101B2D;
    font-size: 21px;
    font-weight: 700;
    border-left: 5px solid #C5A15B;
    padding-left: 13px;
    margin-top: 15px;
    margin-bottom: 12px;
}

/* Information panel */
.info-panel {
    background: #FFFFFF;
    border: 1px solid #DED9CB;
    border-left: 5px solid #C5A15B;
    border-radius: 8px;
    padding: 17px 20px;
    margin: 18px 0 25px 0;
    color: #263C50;
}

/* Form container */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E1DED5;
    border-radius: 10px;
    padding: 24px;
}

/* Input labels */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    color: #263C50;
    font-weight: 600;
}

/* Buttons */
.stFormSubmitButton > button {
    background-color: #101B2D;
    color: #FFFFFF;
    border: 1px solid #C5A15B;
    border-radius: 7px;
    min-height: 46px;
    font-weight: 700;
}

.stFormSubmitButton > button:hover {
    background-color: #263C50;
    color: #FFFFFF;
    border: 1px solid #C5A15B;
}

/* Result cards */
.result-card {
    background: #FFFFFF;
    border: 1px solid #DED9CB;
    border-top: 4px solid #C5A15B;
    border-radius: 9px;
    padding: 20px;
    min-height: 125px;
}

.result-label {
    color: #64748B;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.result-value {
    color: #101B2D;
    font-size: 25px;
    font-weight: 750;
    margin-top: 12px;
}

.result-description {
    color: #64748B;
    font-size: 13px;
    margin-top: 5px;
}

/* Divider */
hr {
    border-color: #DED9CB;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. LOAD MACHINE LEARNING MODELS
# ==================================================

@st.cache_resource
def load_models():

    satisfaction = joblib.load(SATISFACTION_MODEL)
    escalation = joblib.load(ESCALATION_MODEL)

    return satisfaction, escalation


try:

    satisfaction_model, escalation_model = load_models()

except FileNotFoundError as error:

    st.error(f"Required model file not found: {error}")
    st.stop()

except Exception as error:

    st.error(f"Could not load models: {error}")
    st.stop()


# ==================================================
# 4. EXTRACT MODEL INPUT FEATURES
# ==================================================

preprocessor = satisfaction_model.named_steps["preprocessor"]

numeric_features = list(preprocessor.transformers_[0][2])
categorical_features = list(preprocessor.transformers_[1][2])

numeric_imputer = (
    preprocessor.named_transformers_["numeric"]
    .named_steps["imputer"]
)

categorical_encoder = (
    preprocessor.named_transformers_["categorical"]
    .named_steps["encoder"]
)

numeric_defaults = dict(
    zip(numeric_features, numeric_imputer.statistics_)
)

category_options = {
    feature: [str(value) for value in categories]
    for feature, categories in zip(
        categorical_features,
        categorical_encoder.categories_
    )
}

feature_order = list(preprocessor.feature_names_in_)

if feature_order != list(escalation_model.feature_names_in_):

    st.error("The two models have different input features.")
    st.stop()


def display_name(feature):
    return feature.replace("_", " ").title()


# ==================================================
# 5. GOVERNMENT PORTAL HEADER
# ==================================================

st.html("""
<div style="
    background: linear-gradient(110deg, #101B2D, #263C50);
    border-bottom: 5px solid #C5A15B;
    border-radius: 10px;
    padding: 30px 32px;
    margin-bottom: 22px;
    color: white;
">

    <div style="
        color: #D8BD83;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    ">
        MUNICIPAL GOVERNANCE & INTELLIGENCE PORTAL
    </div>

    <h1 style="
        color: #FFFFFF;
        font-size: 30px;
        margin-top: 12px;
        margin-bottom: 8px;
    ">
        Smart Civic Complaint Intelligence
    </h1>

    <p style="
        color: #E0E5EC;
        font-size: 15px;
        margin-bottom: 5px;
    ">
        Intelligence for Better Governance.
        Transparency for Better Cities.
    </p>

    <div style="
        color: #D8BD83;
        font-size: 12px;
        margin-top: 17px;
        letter-spacing: 1px;
    ">
        CITIZEN SERVICES | CIVIC DATA | SMART GOVERNANCE
    </div>

</div>
""")


st.html("""
<div style="
    background: #FFFFFF;
    border: 1px solid #DED9CB;
    border-left: 5px solid #C5A15B;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 24px;
">

    <div style="
        color: #101B2D;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 5px;
    ">
        Civic Intelligence Service
    </div>

    <div style="
        color: #526273;
        font-size: 14px;
    ">
        Analyse civic complaint information using experimental
        machine learning models trained on historical data.
    </div>

</div>
""")


# ==================================================
# 6. COMPLAINT INPUT FORM
# ==================================================

st.markdown(
    '<div class="section-title">Complaint Information</div>',
    unsafe_allow_html=True
)

st.caption(
    "Enter the available complaint details to generate "
    "satisfaction and escalation predictions."
)

with st.form("complaint_form"):

    st.markdown("#### 01 — Numerical Information")

    inputs = {}

    left_column, right_column = st.columns(2)

    for index, feature in enumerate(numeric_features):

        column = left_column if index % 2 == 0 else right_column

        with column:

            inputs[feature] = st.number_input(
                display_name(feature),
                value=float(numeric_defaults[feature]),
                step=1.0,
                format="%.2f",
                key=f"numeric_{feature}"
            )

    st.divider()

    st.markdown("#### 02 — Complaint Classification")

    left_column, right_column = st.columns(2)

    for index, feature in enumerate(categorical_features):

        column = left_column if index % 2 == 0 else right_column

        with column:

            inputs[feature] = st.selectbox(
                display_name(feature),
                options=category_options[feature],
                key=f"category_{feature}"
            )

    st.divider()

    submitted = st.form_submit_button(
        "Analyse Complaint",
        type="primary",
        use_container_width=True
    )


# ==================================================
# 7. GENERATE PREDICTIONS
# ==================================================

if submitted:

    input_df = pd.DataFrame(
        [[inputs[feature] for feature in feature_order]],
        columns=feature_order
    )

    try:

        # Satisfaction prediction
        satisfaction_prediction = int(
            satisfaction_model.predict(input_df)[0]
        )

        satisfaction_probabilities = (
            satisfaction_model.predict_proba(input_df)[0]
        )

        satisfaction_classes = list(satisfaction_model.classes_)

        satisfied_index = satisfaction_classes.index(1)

        satisfaction_probability = float(
            satisfaction_probabilities[satisfied_index]
        )

        # Escalation prediction
        escalation_prediction = int(
            escalation_model.predict(input_df)[0]
        )

        escalation_probabilities = (
            escalation_model.predict_proba(input_df)[0]
        )

        escalation_classes = list(escalation_model.classes_)

        escalation_index = escalation_classes.index(1)

        escalation_probability = float(
            escalation_probabilities[escalation_index]
        )

    except Exception as error:

        st.error(f"Prediction could not be generated: {error}")
        st.stop()


    # ==================================================
    # 8. DISPLAY ANALYSIS RESULTS
    # ==================================================

    st.divider()

    st.markdown(
        '<div class="section-title">Complaint Analysis Report</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Results generated by the trained satisfaction "
        "and escalation machine learning models."
    )

    # Satisfaction
    st.markdown("#### 01 — Citizen Satisfaction Analysis")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">Predicted Outcome</div>',
                unsafe_allow_html=True
            )

            if satisfaction_prediction == 1:
                st.success("Satisfied")
            else:
                st.warning("Not Satisfied")

            st.caption("Model classification")

    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">'
                'Estimated Satisfaction Probability'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="result-value">'
                f'{satisfaction_probability * 100:.1f}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.progress(satisfaction_probability)

    st.info(
        "This probability is a model-generated estimate, "
        "not a guarantee. The satisfaction model has limited "
        "validation performance."
    )

    # Escalation
    st.markdown("#### 02 — Complaint Escalation Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">Predicted Outcome</div>',
                unsafe_allow_html=True
            )

            if escalation_prediction == 1:
                st.warning("Escalation")
            else:
                st.success("No Escalation")

            st.caption("Model classification")

    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">'
                'Estimated Escalation Probability'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="result-value">'
                f'{escalation_probability * 100:.1f}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.progress(escalation_probability)

    st.warning(
        "The escalation model has weak validation performance. "
        "This experimental prediction must not be used for "
        "actual complaint prioritisation or municipal decisions."
    )

    # Submitted information
    with st.expander("View Complete Complaint Details"):

        st.dataframe(
            input_df.T.rename(columns={0: "Entered Value"}),
            use_container_width=True
        )


# ==================================================
# 9. GOVERNMENT PORTAL FOOTER
# ==================================================

st.html("""
<div style="
    text-align: center;
    padding: 20px;
    margin-top: 20px;
    border-top: 1px solid #DED9CB;
    color: #64748B;
    font-size: 12px;
">

    <strong style="color: #263C50;">
        SMART CIVIC COMPLAINT INTELLIGENCE
    </strong>

    <br><br>

    Academic Demonstration Prototype |
    Not an Official Municipal Service

</div>
""")