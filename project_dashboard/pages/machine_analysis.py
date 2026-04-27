# TODO: Data Acquistion (DONE)
# TODO: Data Preprocessing of Chosen Dataframes
# TODO: Feature Selection of
# TODO: Define classifcation task
# TODO: Test both RandomForest and XGBoost to determine
# TODO: Generation of confusion matrix
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import plotly.express as px

current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to 'project_dashboard', then into 'models'
# This creates the path: /.../project_dashboard/models/cases_model.pkl
cases_path = os.path.join(current_dir, "..", "models", "cases_model.pkl")
deaths_path = os.path.join(current_dir, "..", "models", "deaths_model.pkl")
scaler_path = os.path.join(current_dir, "..", "models", "age_scaler.pkl")

# 3. Load using the dynamic paths
try:
    cases_model = joblib.load(cases_path)
    deaths_model = joblib.load(deaths_path)
    scaler = joblib.load(scaler_path)
except FileNotFoundError as e:
    st.error(f"Could not find model files. Looked in: {cases_path}")
    st.stop()  # Stops the app execution so you don't get more errors
# 1. Load the saved assets
# Ensure these paths are correct based on your folder structure!

# List of states exactly as they appeared in your training columns
STATES = [
    "Johor",
    "Kedah",
    "Kelantan",
    "Melaka",
    "Negeri Sembilan",
    "Pahang",
    "Perak",
    "Perlis",
    "Pulau Pinang",
    "Sabah",
    "Sarawak",
    "Selangor",
    "Terengganu",
    "W.P. Kuala Lumpur",
    "W.P. Labuan",
    "W.P. Putrajaya",
]

st.title("🇲🇾 KKMNow COVID-19 Prediction Dashboard")

mode = st.sidebar.selectbox(
    "Select Model", ["Daily Cases Forecast", "Individual Death Risk (BID)"]
)
if mode == "Daily Cases Forecast":
    st.header("Predict New Daily Cases")

    # Add inputs for the missing features
    c_import = st.number_input("Cases Import", min_value=0, value=0)
    c_recovered = st.number_input("Cases Recovered", min_value=0, value=0)
    active = st.number_input("Current Active Cases", min_value=0)
    cluster = st.number_input("Cluster Cases", min_value=0)
    selected_state = st.selectbox("State", STATES)

    if st.button("Forecast New Cases"):
        state_bits = [1 if s == selected_state else 0 for s in STATES]

        # Combine everything into a single list
        # Ensure this order matches your X_train_c.columns exactly!
        feature_list = [c_import, c_recovered, active, cluster] + state_bits

        input_data = np.array([feature_list])

        # Now this will have 20 features
        prediction = cases_model.predict(input_data)
        st.success(f"Predicted New Cases: {int(prediction[0])}")
    if hasattr(cases_model, "feature_importances_"):
        st.subheader("What's Driving the Forecast?")
        feat_names = ["Cases Import", "Recovered", "Active", "Cluster"] + STATES
        importances = cases_model.feature_importances_
        df_imp = pd.DataFrame({"Feature": feat_names, "Importance": importances})
        df_imp = df_imp.sort_values("Importance", ascending=True).tail(10)  # Top 10

        fig_imp = px.bar(
            df_imp,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 10 Drivers of New Cases",
        )
        st.plotly_chart(fig_imp, use_container_width=True)

elif mode == "Individual Death Risk (BID)":
    st.header("Classify Death Circumstance (BID vs Hospital)")

    age = st.slider("Patient Age", 0, 100, 45)
    male_val = 1 if st.radio("Sex", ["Male", "Female"]) == "Male" else 0
    malaysian_val = 1 if st.checkbox("Is Malaysian?") else 0
    comorb_val = 1 if st.checkbox("Has Comorbidities?") else 0
    selected_state = st.selectbox("State", STATES)

    if st.button("Predict Outcome"):
        # 1. Scale Age
        scaled_age = scaler.transform([[age]])[0][0]

        # 2. Prepare features (Age, Male, Malaysian, Comorb, 16 State Booleans)
        state_bits = [1 if s == selected_state else 0 for s in STATES]
        features = np.array(
            [[scaled_age, male_val, malaysian_val, comorb_val] + state_bits]
        )

        # DEFINING RESULT HERE
        result = deaths_model.predict(features)[0]

        if result == 1:
            st.error("Predicted Status: Brought In Dead (BID)")
        else:
            st.success("Predicted Status: Hospital Death")
        probs = deaths_model.predict_proba(features)[0]
        bid_probability = probs[1] * 100  # Probability of class 1 (BID)

        import plotly.graph_objects as go

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=bid_probability,
                title={"text": "BID Risk Probability (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkred" if bid_probability > 50 else "darkblue"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 100], "color": "gray"},
                    ],
                },
            )
        )

        st.plotly_chart(fig_gauge, use_container_width=True)
