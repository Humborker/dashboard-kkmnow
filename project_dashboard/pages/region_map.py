import streamlit as st
import plotly.express as px
from dataloader import load_project_data
import geopandas as gd
import pandas as pd
import os

# TODO: geopandas (mapping tool)

path = "../project_dashboard/datasets"
if os.path.exists(path):
    map_df = load_project_data(path)


st.title("Region Map")


def get_geo_type(df):
    """Detects which geographic columns are available."""
    cols = df.columns.tolist()
    if "Direction" in cols:
        return "compass"
    elif "Country" in cols or "State" in cols:
        return "name_based"
    else:
        return "non_geo"


# Inside your Streamlit app:
selected_key = st.sidebar.selectbox("Select Dataset", list(map_df.keys()))
df = map_df[selected_key]

geo_status = get_geo_type(df)

if geo_status == "compass":
    fig = px.box(df, x="Direction", y="Value", color="Direction")
    st.plotly_chart(fig)
# Compass Map (To be filled.)
COMPASS_MAP = {
    #    "Canada": "North",
    #    "USA": "North",
    #    "Brazil": "South",
    #    "Australia": "South",
}

if geo_status == "name_based":
    # Create the column on the fly
    target_col = "Country" if "Country" in df.columns else "State"
    df["Direction"] = df[target_col].map(COMPASS_MAP).fillna("Unknown")

    fig = px.scatter(df, x="Direction", y="Value", hover_name=target_col)
    st.plotly_chart(fig)

if geo_status == "non_geo":
    st.warning("This dataset does not contain regional mapping data.")
    # Fallback to a standard line plot or table
    st.line_chart(df)

tab1, tab2 = st.tabs(["Visualization", "Raw Data"])

with tab1:
    if geo_status != "non_geo":
        st.subheader(f"Regional Analysis: {selected_key}")
        # Your Plotly logic here
    else:
        st.info("General Trend Analysis (Non-Regional)")
        # General plot

with tab2:
    st.dataframe(df)
