import streamlit as st
from dataloader import load_project_data
import pandas as pd

st.title("Region Map")


def assign_region(row, center_lat, center_long):
    """Assigns a compass direction based on relative coordinates."""
    n_s = "North" if row["lat"] >= center_lat else "South"
    e_w = "East" if row["lon"] >= center_long else "West"

    return f"{n_s}-{e_w}"


# Example Data
data = {
    "Country": ["Norway", "South Africa", "Japan", "Brazil"],
    "lat": [60.47, -30.55, 36.20, -14.23],
    "lon": [8.46, 22.93, 138.25, -51.92],
}

df = pd.DataFrame(data)

# Define "Center" (e.g., Near the Prime Meridian/Equator intersection)
CENTER_LAT, CENTER_LON = 0, 0

# Apply mapping
df["Region"] = df.apply(assign_region, axis=1, args=(CENTER_LAT, CENTER_LON))
