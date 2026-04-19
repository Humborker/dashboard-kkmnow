import os
import streamlit as st
from dataloader import load_project_data

st.title("Data Explorer")

path = "../project_dashboard/datasets"
if os.path.exists(path):
    all_dfs = load_project_data(path)

    st.sidebar.success(f"Loaded {len(all_dfs)} dataframes from cache.")

    target_df = st.sidebar.selectbox(
        "Select Data to View", options=list(all_dfs.keys())
    )
    df = all_dfs[target_df]

    st.header(f"Dataset: {target_df}")
    st.dataframe(all_dfs[target_df].head(10))
    st.subheader("Summary Statistics")
    st.write(df.describe())


else:
    st.error(f"Directory '{path}' not found. Please check your file path.")
