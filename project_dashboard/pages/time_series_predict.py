import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from dataloader import load_project_data
import joblib
import os
from prophet import Prophet
from prophet.plot import plot_plotly

# TODO: Hit 80% using scikit machine learning (LOL function)
# TODO:
# TODO: Use deep learning.
# TODO:
path = "../project_dashboard/datasets"
if os.path.exists(path):
    map_df = load_project_data(path)

# 1. Load your KKM dictionary dataframe

# --- 1. Selection Logic ---
st.title("📈 KKM Health Forecaster")


def trend_predictor():
    # Let the user pick which DataFrame from your dictionary to use
    dataset_key = st.selectbox("1. Choose a Dataset", options=list(map_df.keys()))
    active_df = map_df[dataset_key].copy()

    # Prophet needs a date column. Let's find it.
    # We'll assume your KKM data has a 'date' column.
    if "date" in active_df.columns:
        active_df["date"] = pd.to_datetime(active_df["date"])

        # 2. Select specific metric (y-axis) from that chosen DataFrame
        numeric_cols = active_df.select_dtypes(include=["number"]).columns
        target_metric = st.selectbox(
            "2. Select Metric to Forecast", options=numeric_cols
        )

        # 3. Forecast Configuration
        days_to_pred = st.slider("Forecast Horizon (Days)", 7, 90, 30)

        # --- 2. Prophet Integration ---
        if st.button("Run Forecast"):
            with st.spinner(f"Analyzing {dataset_key}..."):
                # Prepare data: Prophet expects 'ds' and 'y'
                # We'll filter for Malaysia-wide data for a cleaner forecast
                if "state" in active_df.columns:
                    df_prep = active_df[active_df["state"] == "Malaysia"]
                else:
                    df_prep = active_df

                df_prophet = (
                    df_prep[["date", target_metric]]
                    .rename(columns={"date": "ds", target_metric: "y"})
                    .dropna()
                )

                # Initialize and Train
                model = Prophet(weekly_seasonality=True, yearly_seasonality=True)
                model.fit(df_prophet)

                # Create Future DataFrame
                future = model.make_future_dataframe(periods=days_to_pred)
                forecast = model.predict(future)

                # --- 3. Visualization ---
                st.subheader(f"Future Outlook: {target_metric}")

                # Use plot_plotly for interactive Streamlit charts
                fig = plot_plotly(model, forecast)
                fig.update_layout(
                    title=f"{dataset_key} Forecast", yaxis_title=target_metric
                )
                st.plotly_chart(fig, use_container_width=True)

                # Show components (Trend, Seasonality)
                with st.expander("View Forecast Components"):
                    fig_comp = model.plot_components(forecast)
                    st.write(fig_comp)
    else:
        st.error("The selected dataset does not have a 'date' column.")


if __name__ == "__main__":
    trend_predictor()
