import plotly.express as px
import seaborn as sns
import streamlit as st
from dataloader import load_project_data


def load_data():
    # Loading from seaborn's built-in datasets
    df = sns.load_dataset("iris")
    return df


def run_vis_page():
    st.title("KKM Data Visualization")
    df = load_data()

    # --- Sidebar Filters ---
    st.sidebar.header("Visualization Settings")

    chart_type = st.sidebar.radio(
        "Select Chart Type",
        (
            "Scatter Plot",
            "Distribution (Histogram)",
            "Violin Plot",
            "Bar Plot",
            "Line Plot",
            "Box Plot",
        ),
    )

    features = df.columns[:-1].tolist()

    # --- Main Visualization Logic ---
    if chart_type == "Scatter Plot":
        st.subheader("Feature Comparison")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", features, index=0)
        with col2:
            y_axis = st.selectbox("Y-Axis", features, index=1)

        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            color="species",
            symbol="species",
            hover_name="species",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Distribution (Histogram)":
        st.subheader("Feature Distributions")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.histogram(
            df,
            x=selected_feature,
            color="species",
            marginal="box",  # Adds a boxplot on top
            barmode="overlay",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Violin Plot":
        st.subheader("Feature Density by Species")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.violin(
            df,
            y=selected_feature,
            x="species",
            color="species",
            box=True,
            points="all",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Plot":
        st.subheader("Feature Density by Species")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.violin(
            df,
            y=selected_feature,
            x="species",
            color="species",
            box=True,
            points="all",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Line Plot":
        st.subheader("Feature Density by Species")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.violin(
            df,
            y=selected_feature,
            x="species",
            color="species",
            box=True,
            points="all",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        st.subheader("Feature Density by Species")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.violin(
            df,
            y=selected_feature,
            x="species",
            color="species",
            box=True,
            points="all",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Summary Statistics ---
    with st.expander("View Raw Data & Summary Stats"):
        st.dataframe(df.describe(), use_container_width=True)
        st.write("Full Dataset:", df)


if __name__ == "__main__":
    run_vis_page()
