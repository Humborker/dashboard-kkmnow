import streamlit as st
import pandas as pd
from pathlib import Path
import os

# NOTE: Broad dataloader function across all pages.
# TODO: Institute broader functions for pages


@st.cache_data
def load_project_data(directory):
    df_dict = {}
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(directory, file)
        # Use the filename (without .csv) as the dictionary key
        name = file.replace(".csv", "")
        df_dict[name] = pd.read_csv(file_path)

    return df_dict
