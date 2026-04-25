import streamlit as st
import plotly.express as px
from dataloader import load_project_data
import geopandas as gd
import pandas as pd
import os
import json

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = "../project_dashboard/datasets"
map_path = os.path.join(BASE_DIR, "..", "map_data", "malaysia.json")

# 1. Load GeoJSON as a DICTIONARY (much faster than GDF)


@st.cache_data
def load_geojson_data():
    with open(map_path, "r") as f:
        return json.load(f)


# 2. Load CSV Data
if os.path.exists(path):
    map_df = load_project_data(path)

malaysia_geojson = load_geojson_data()


def run_map_page():
    st.sidebar.header("Map Configuration")

    selected_dataset = st.sidebar.selectbox(
        "Select Dataset", options=list(map_df.keys())
    )
    active_df = map_df[selected_dataset]

    metric_to_plot = st.sidebar.selectbox(
        "Select Metric", options=active_df.select_dtypes(include=["number"]).columns
    )

    st.subheader(f"Mapping {selected_dataset}: {metric_to_plot}")

    # 3. Plotly Express Choropleth
    # We use active_df (Pandas) directly, NOT a merged GeoDataFrame
    fig = px.choropleth(
        active_df,
        geojson=malaysia_geojson,
        locations="state",  # Column in active_df
        featureidkey="properties.name",  # Path to the name inside the GeoJSON 'properties'
        color=metric_to_plot,
        color_continuous_scale="YlOrRd",
        projection="mercator",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    run_map_page()
