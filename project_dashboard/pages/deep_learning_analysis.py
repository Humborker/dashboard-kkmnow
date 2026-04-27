import streamlit as st
import tensorflow as tf
import numpy as np
import os

# --- PATHING LOGIC ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Note the ".." to go up from 'pages/' into the root, then into 'models/'
cases_path = os.path.join(current_dir, "..", "models", "case_model.keras")
deaths_path = os.path.join(current_dir, "..", "models", "deaths_model.keras")

# --- MODEL LOADING (CACHED) ---


@st.cache_resource
def load_tf_models():
    return tf.keras.models.load_model(cases_path), tf.keras.models.load_model(
        deaths_path
    )


cases_nn, deaths_nn = load_tf_models()

st.title("🧠 Neural Network Analysis")
st.write("Independent Deep Learning models for Cases and Deaths.")

# --- TABS FOR ORGANIZATION ---
tab1, tab2 = st.tabs(["Regression (Cases)", "Classification (Deaths)"])

with tab1:
    st.subheader("Predict Daily New Cases")
    # Inputs (Ensure these match your 20 training features)
    c_import = st.number_input("Cases Import", min_value=0)
    c_recovered = st.number_input("Cases Recovered", min_value=0)
    active = st.number_input("Active Cases", min_value=0)
    cluster = st.number_input("Cluster Cases", min_value=0)
    # ... add your state selection logic here ...

    if st.button("Run Keras Regression"):
        # NN expects float32 and exact shapes
        input_data = np.array(
            [[c_import, c_recovered, active, cluster] + [0] * 16], dtype="float32"
        )
        prediction = cases_nn.predict(input_data)
        st.metric("Predicted New Cases", int(prediction[0][0]))

with tab2:
    st.subheader("Predict BID Probability")
    age = st.slider("Age", 0, 100, 50)
    comorb = st.checkbox("Comorbidities")

    if st.button("Run Keras Classification"):
        # Standardize Age here if you did it during training!
        input_data = np.array([[age, 1, 1, int(comorb)] + [0] * 16], dtype="float32")

        # Sigmoid output is a probability between 0 and 1
        prob = deaths_nn.predict(input_data)[0][0]

        if prob > 0.5:
            st.error(f"Prediction: BID (Probability: {prob:.2%})")
        else:
            st.success(f"Prediction: Hospital (Probability: {prob:.2%})")
