import streamlit as st
import pandas as pd
from forecasting_engine import forecast

def main():
    st.title("Financial Forecasting Dashboard")
    
    uploaded_file = st.file_uploader("Upload financial data (CSV/Excel)")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())
        
        if st.button("Run Forecast"):
            forecast_results = forecast(df)
            st.line_chart(forecast_results)
            st.download_button("Download Forecast", forecast_results.to_csv(), "forecast_results.csv")
    
    st.sidebar.header("Scenario Analysis")
    scenarios = {
        'Optimistic': st.sidebar.slider("Optimistic", 0.5, 2.0, 1.2),
        'Base': st.sidebar.slider("Base", 0.5, 2.0, 1.0),
        'Pessimistic': st.sidebar.slider("Pessimistic", 0.5, 2.0, 0.8)
    }

if __name__ == "__main__":
    main()
