# streamlit_app.py

import streamlit as st
import pandas as pd
from forecasting_engine import run_forecasting_model  # Your function from forecasting_engine.py

st.set_page_config(page_title="Forecasting AI", layout="wide")

st.title("📊 AI-Powered Forecasting Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv", "xlsx", "json"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        df = pd.read_json(uploaded_file)
    
    st.write("📁 Uploaded Data Preview:")
    st.dataframe(df.head())

    st.markdown("---")
    st.write("🔮 Forecasting Results:")
    
    # Forecast and show results
    forecast_df, model_used, metrics = run_forecasting_model(df)
    
    st.success(f"Model Used: {model_used}")
    st.dataframe(forecast_df.tail())

    st.markdown("📉 Forecast Plot:")
    st.line_chart(forecast_df.set_index("date"))

    st.markdown("📏 Evaluation Metrics:")
    st.write(metrics)

else:
    st.info("Please upload a data file to begin.")
