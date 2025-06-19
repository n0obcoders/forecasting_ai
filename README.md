Financial Forecasting System - User Guide

1. SETUP
   - Install requirements: pip install -r requirements.txt
   - Create data/data.csv with your financial data

2. DATA PREPARATION
   Required columns: date (YYYY-MM-DD format)
   At least one of: revenue, sales, expenses, profit, cashflow, demand
   
   Sample structure:
   date,revenue,expenses
   2023-01-01,10000,6000
   2023-02-01,12000,6500

3. RUNNING FORECASTS
   Option A: Streamlit Dashboard
     streamlit run dashboard.py
   
   Option B: Command Line
     from forecasting_engine import forecast
     import pandas as pd
     
     df = pd.read_csv('data/sample_financial_data.csv')
     results = forecast(df, target_col='revenue')

4. QUALITATIVE FORECASTING
   - Use the Delphi method in the dashboard sidebar
   - Set scenario multipliers for best/most-likely/worst cases
   - Provide expert confidence scores (0-100)

5. MODEL SELECTION
   - Auto-selection: System chooses best model based on data
   - Manual selection: Specify model_type parameter:
        moving_average
        exponential_smoothing
        linear_regression
        arima
        prophet
        lstm
        qualitative

6. EVALUATION
   - System calculates MAE and RMSE automatically
   - Use evaluate_models() to compare all models
   - Best models are highlighted in green (MAE) and blue (RMSE)

7. OUTPUT
   - Interactive charts in dashboard
   - Downloadable CSV reports
   - Model accuracy metrics
