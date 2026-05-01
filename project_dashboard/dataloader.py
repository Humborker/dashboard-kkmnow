import streamlit as st
import pandas as pd
from pathlib import Path
import os
import functools

# NOTE: Broad dataloader function across all pages.
# TODO: Institute broader functions for pages


@st.cache_data
def get_merged_df(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    dfs = []

    for file in files:
        df = pd.read_csv(os.path.join(directory, file))
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            # We suffix columns so we know which file they came from
            # e.g., 'cases_new' becomes 'cases_new (cases_malaysia)'
            suffix = f" ({file.replace('.csv', '')})"
            df = df.set_index("date").add_suffix(suffix).reset_index()
            dfs.append(df)

    # Merge all dataframes on the 'date' column
    if dfs:
        df_merged = functools.reduce(
            lambda left, right: pd.merge(left, right, on="date", how="outer"), dfs
        )
        return df_merged.sort_values("date")
    return pd.DataFrame()


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
