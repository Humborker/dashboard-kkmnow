import os
import seaborn as sns
import plotly.express as px
import streamlit as st
from dataloader import load_project_data


path = "../project_dashboard/datasets"
if os.path.exists(path):
    df = load_project_data(path)


def run_vis_page():
    st.title("KKM Data Visualization")
    # --- Sidebar Filters ---
    st.sidebar.header("Visualization Settings")

    chart_type = st.sidebar.radio(
        "Select Chart Type",
        (
            "Scatter Plot",
            "Distribution (Histogram)",
            "Bar Plot",
            "Line Plot",
            "Box Plot",
        ),
    )
    dataset_name = st.sidebar.selectbox("Select Dataset", options=list(df.keys()))

    vis_df = df[dataset_name]

    # 4. Now you can safely access .columns because 'df' is a DataFrame
    features = vis_df.columns.tolist()

    # --- Main Visualization Logic ---
    if chart_type == "Scatter Plot":
        st.subheader("Feature Comparison")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", features, index=0)
        with col2:
            y_axis = st.selectbox("Y-Axis", features, index=1)

        fig = px.scatter(
            vis_df,
            x=x_axis,
            y=y_axis,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Distribution (Histogram)":
        st.subheader("Feature Distributions")
        selected_feature = st.selectbox("Select Feature", features)

        fig = px.histogram(
            vis_df,
            x=selected_feature,
            marginal="box",  # Adds a boxplot on top
            barmode="overlay",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", features, index=0)
        with col2:
            y_axis = st.selectbox("Y-Axis", features, index=1)

        fig = px.bar(
            vis_df,
            y=y_axis,
            x=x_axis,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Line Plot":
        selected_feature = st.selectbox("Select Feature", features)
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", features, index=0)
        with col2:
            y_axis = st.selectbox("Y-Axis", features, index=1)

        fig = px.line(
            vis_df,
            x=x_axis,
            y=y_axis,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", features, index=0)
        with col2:
            y_axis = st.selectbox("Y-Axis", features, index=1)

        fig = px.box(
            vis_df,
            y=y_axis,
            x=x_axis,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Summary Statistics ---
    with st.expander("View Raw Data & Summary Stats"):
        st.dataframe(vis_df.describe(), use_container_width=True)
        st.write("Full Dataset:", df)


if __name__ == "__main__":
    run_vis_page()
