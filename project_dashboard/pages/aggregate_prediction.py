import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dataloader import load_project_data, get_merged_df

# 1. Load the data
path = "../project_dashboard/datasets"
# Unmerged dataset
if os.path.exists(path):
    all_data = load_project_data(path)


def aggregate_data():
    if not all_data:
        st.error("No CSV files found in the specified directory.")
    else:
        # 2. Sidebar Selection
        st.sidebar.header("Data Selection")
        selected_name = st.sidebar.selectbox(
            "Choose a Dataset to Visualize", options=list(all_data.keys())
        )

        # 3. Retrieve the selected DataFrame
        df = all_data[selected_name]

        st.title(f"Analysis: {selected_name.replace('_', ' ').title()}")

        # 4. Dynamic Column Selection for Time Series
        # Assuming KKMNow format, we look for 'date' and numeric columns
        columns = df.columns.tolist()

        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox(
                "X-Axis (usually 'date')",
                options=columns,
                index=columns.index("date") if "date" in columns else 0,
            )
        with col2:
            # Filter for numeric columns for the Y-axis
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            y_axis = st.selectbox("Y-Axis (Metric)", options=numeric_cols)

        # 5. Render the Chart
        if x_axis and y_axis:
            fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

        # 6. Optional: Show raw data
        with st.expander("View Raw Data"):
            st.dataframe(df)


if __name__ == "__main__":
    aggregate_data()
