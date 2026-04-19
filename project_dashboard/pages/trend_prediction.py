import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from dataloader import load_project_data

st.title("Trend_Prediction")

# 1. App Configuration
st.set_page_config(page_title="Iris Species Predictor", page_icon="🌱")


@st.cache_resource
def load_model():
    """Load the Iris dataset and train a simple Random Forest model."""
    iris = datasets.load_iris()
    X = iris.data
    Y = iris.target

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, Y)


# Initialize model and data
model, target_names, feature_names = load_model()

# 2. Sidebar UI - User Input
st.sidebar.header("Input Features")
st.sidebar.markdown("Adjust the sliders to predict the Iris species.")


def user_input_features():
    sepal_length = st.sidebar.slider("Sepal length", 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider("Sepal width", 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider("Petal length", 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider("Petal width", 0.1, 2.5, 0.2)

    data = {
        "sepal length (cm)": sepal_length,
        "sepal width (cm)": sepal_width,
        "petal length (cm)": petal_length,
        "petal width (cm)": petal_width,
    }
    return pd.DataFrame(data)


df_input = user_input_features()

# 3. Main Page UI
st.title("Iris Flower Classification")
st.write("""
This app predicts the **Iris flower** type based on its morphology.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("User Input Parameters")
    st.write(df_input)

# 4. Prediction Logic
prediction = model.predict(df_input)
prediction_proba = model.predict_proba(df_input)

with col2:
    st.subheader("Prediction")
    predicted_species = target_names[prediction][0]
    st.success(f"**{predicted_species.capitalize()}**")

# 5. Probability Visualization
st.divider()
st.subheader("Prediction Probability")
proba_df = pd.DataFrame(prediction_proba, columns=target_names)
st.bar_chart(proba_df.T)

st.info(f"The model is most confident that this is a **{predicted_species}**.")
