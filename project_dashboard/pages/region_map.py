import streamlit as st
import plotly.express as px
from dataloader import load_project_data
import geopandas as gd
import pandas as pd
import os

# DONE: geopandas (mapping tool)
# TODO: resolve massive fucking latency issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = "../project_dashboard/datasets"
map_path = os.path.join(BASE_DIR, "..", "map_data", "malaysia.json")
# map_path = "../map_data/malaysia.geojson"
if os.path.exists(path):
    map_df = load_project_data(path)


st.title("Region Map")

# 2. Load the Spatial Data (GeoJSON/Shapefile)


@st.cache_data
def load_geo():
    # Ensure this file exists in your project directory
    gdf = gd.read_file(map_path)
    return gdf


gdf_states = load_geo()
gdf_states = gdf_states.drop(columns=["source", "id"])
gdf_states["geometry"] = gdf_states["geometry"].simplify(
    tolerance=0.01, preserve_topology=True
)
print(gdf_states.columns.unique())


def run_map_page():
    st.sidebar.header("Map Configuration")

    # Choose which CSV from the dictionary
    selected_dataset = st.sidebar.selectbox(
        "Select Dataset", options=list(map_df.keys())
    )

    # Get the specific DataFrame from the dictionary
    active_df = map_df[selected_dataset]

    # Choose which column from that CSV to visualize
    metric_to_plot = st.sidebar.selectbox(
        "Select Metric", options=active_df.select_dtypes(include=["number"]).columns
    )

    # 4. Merging Logic
    # We merge the GeoDataFrame with the selected DataFrame from your dictionary
    # Adjust 'state_name' and 'state' to match your specific file column names
    merged_data = gdf_states.merge(
        active_df, left_on="name", right_on="state", how="left"
    )

    # 5. Rendering the Map
    st.subheader(f"Mapping {selected_dataset}: {metric_to_plot}")

    fig = px.choropleth(
        merged_data,
        geojson=merged_data.geometry,
        locations=merged_data.index,
        color=metric_to_plot,
        hover_name="state",
        color_continuous_scale="YlOrRd",
        projection="mercator",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    run_map_page()
