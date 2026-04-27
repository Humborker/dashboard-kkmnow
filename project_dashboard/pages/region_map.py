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


exclude_files = ["metadata.csv", "linelist_deaths.csv"]
# 2. Load CSV Data
if os.path.exists(path):
    map_df = load_project_data(path)
    map_df.pop("blood_donations", None)
    map_df.pop("infant_immunisation", None)
    map_df.pop("blood_donations", None)


malaysia_geojson = load_geojson_data()


def run_map_page():
    st.sidebar.header("Map Configuration")

    selected_dataset = st.sidebar.selectbox(
        "Select Dataset", options=list(map_df.keys())
    )
    active_df = map_df[selected_dataset].copy()

    # Get numeric columns for the user to choose from
    numeric_cols = active_df.select_dtypes(include=["number"]).columns
    metric_to_plot = st.sidebar.selectbox("Select Metric", options=numeric_cols)

    # --- NEW: AGGREGATION LOGIC ---
    # Group by state and calculate the mean
    # This turns binary [0, 1] into a decimal proportion (e.g., 0.75)
    map_ready_df = active_df.groupby("state")[metric_to_plot].mean().reset_index()

    # --- NEW: SCALE BINARY VALUES ---
    # Check if the column is binary (only contains 0 and 1)
    unique_vals = set(active_df[metric_to_plot].unique())
    is_binary = unique_vals.issubset({0, 1, 0.0, 1.0})

    if is_binary:
        # Scale to 0-100 to represent a percentage for the map
        map_ready_df[metric_to_plot] = map_ready_df[metric_to_plot] * 100
        label_suffix = "(%)"
    else:
        label_suffix = "(Average)"

    st.subheader(f"Mapping {selected_dataset}: {metric_to_plot} {label_suffix}")

    # 3. Plotly Express Choropleth
    fig = px.choropleth(
        map_ready_df,  # Use the aggregated dataframe
        geojson=malaysia_geojson,
        locations="state",
        featureidkey="properties.name",
        color=metric_to_plot,
        color_continuous_scale="YlOrRd",
        # Update labels to reflect if it is a percentage
        labels={metric_to_plot: f"{metric_to_plot} {label_suffix}"},
        projection="mercator",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    run_map_page()
