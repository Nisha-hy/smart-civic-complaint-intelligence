
import joblib
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Civic Complaint Intelligence",
    page_icon="🏙️",
    layout="wide",
)

MODEL_FILE = "civic_satisfaction_model.joblib"


# --------------------------------------------------
# 2. LOAD SAVED MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "Model file not found. Please run train_model.py first."
    )
    st.stop()
except Exception as error:
    st.error(f"Could not load the model: {error}")
    st.stop()


# Retrieve the feature names and categories used during training.
preprocessor = model.named_steps["preprocessor"]

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
        categorical_encoder.categories_,
    )
}

# Preserve the original feature order from training.
feature_order = list(preprocessor.feature_names_in_)


# --------------------------------------------------
# 3. APPLICATION HEADER
# --------------------------------------------------

st.title("🏙️ Smart Civic Complaint Intelligence System")

st.write(
    "Enter the details of a newly registered civic complaint "
    "to estimate the likelihood of citizen satisfaction."
)

st.info(
    "Educational ML prototype. Predictions are experimental "
    "and should not be used to make real civic-service decisions."
)

st.divider()


# --------------------------------------------------
# 4. COMPLAINT INPUT FORM
# --------------------------------------------------

def display_name(feature):
    return feature.replace("_", " ").title()


with st.form("complaint_form"):

    st.subheader("Complaint Details")

    st.caption(
        "Complete the fields below. Numeric defaults are "
        "based on training-data imputation values; edit them "
        "to match the complaint where appropriate."
    )

    inputs = {}

    left_column, right_column = st.columns(2)

    for index, feature in enumerate(numeric_features):
        column = left_column if index % 2 == 0 else right_column

        default_value = float(numeric_defaults[feature])

        with column:
            inputs[feature] = st.number_input(
                display_name(feature),
                value=default_value,
                step=1.0,
                format="%.2f",
                key=f"numeric_{feature}",
            )

    st.divider()
    st.subheader("Complaint Classification")

    left_column, right_column = st.columns(2)

    for index, feature in enumerate(categorical_features):
        column = left_column if index % 2 == 0 else right_column

        options = category_options[feature]

        with column:
            inputs[feature] = st.selectbox(
                display_name(feature),
                options=options,
                key=f"category_{feature}",
            )

    submitted = st.form_submit_button(
        "Predict Citizen Satisfaction",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# 5. PREDICTION
# --------------------------------------------------

if submitted:

    input_df = pd.DataFrame(
        [[inputs[feature] for feature in feature_order]],
        columns=feature_order,
    )

    prediction = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0]

    # Find the probability corresponding to class 1.
    classes = list(model.classes_)
    satisfied_index = classes.index(1)

    satisfaction_probability = float(
        probabilities[satisfied_index]
    )

    st.divider()
    st.subheader("Prediction Result")

    result_column, probability_column = st.columns(2)

    with result_column:
        if prediction == 1:
            st.success("Predicted Outcome: Satisfied")
        else:
            st.warning("Predicted Outcome: Not Satisfied")

    with probability_column:
        st.metric(
            "Estimated Satisfaction Probability",
            f"{satisfaction_probability * 100:.1f}%",
        )

    st.progress(satisfaction_probability)

    st.caption(
        "This probability is a model estimate, not a guarantee "
        "or a verified measure of confidence. The current model "
        "has limited validation performance."
    )

    with st.expander("View submitted complaint details"):
        st.dataframe(
            input_df.T.rename(columns={0: "Entered Value"}),
            use_container_width=True,
        )
