import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import os
from dataloader import load_project_data

path = "../project_dashboard/datasets"
if os.path.exists(path):
    map_df = load_project_data(path)


def forecasting():
    # --- 1. Drilling into the Nested Dictionary ---
    st.sidebar.header("Data Selection")

    # Select the first-level key (e.g., 'Health', 'Economy')
    outer_key = st.sidebar.selectbox("Select Category", options=list(map_df.keys()))

    # Select the second-level key (e.g., 'Hospitalizations', 'Cases')
    inner_key = st.sidebar.selectbox(
        "Select Dataset", options=list(map_df[outer_key].keys())
    )

    # Extract the DataFrame
    active_df = map_df[outer_key][inner_key].copy()

    time_col = active_df.columns[0]
    numeric_cols = active_df.select_dtypes(include=["number"]).columns

    target_y = st.sidebar.selectbox("Select Metric to Forecast", options=numeric_cols)

    # Prepare Prophet Data
    df_prophet = active_df[[time_col, target_y]].rename(
        columns={time_col: "ds", target_y: "y"}
    )
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])

    st.title(f"Forecasting: {inner_key}")
    days_to_pred = st.slider("Forecast Horizon (Days)", 7, 365, 30)

    if st.button("Run Model"):
        with st.spinner("Training Prophet model..."):
            # Initialize and fit
            m = Prophet(changepoint_prior_scale=0.05, daily_seasonality=False)
            m.fit(df_prophet)

            # Predict
            future = m.make_future_dataframe(periods=days_to_pred)
            forecast = m.predict(future)

            # Plotly Interactivity
            fig = plot_plotly(m, forecast)
            st.plotly_chart(fig, use_container_width=True)

            # Display Components
            with st.expander("Show Trend & Seasonality"):
                fig_comp = m.plot_components(forecast)
                st.pyplot(fig_comp)


if __name__ == "__main__":
    forecasting()
