import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# ===== Traditional Models =====
def run_moving_average(df, target_col='target', window=3):
    return df[target_col].rolling(window=window).mean()

def run_exponential_smoothing(df, target_col='target'):
    model = ExponentialSmoothing(df[target_col], seasonal='add', seasonal_periods=12)
    model_fit = model.fit()
    return model_fit.fittedvalues

def run_linear_regression(df, target_col='target'):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    model = LinearRegression()
    model.fit(X, y)
    return model.predict(X)

# ===== Time Series Models =====
def run_arima(df, target_col='target', order=(5,1,0)):
    model = ARIMA(df[target_col], order=order)
    results = model.fit()
    return results.fittedvalues

def run_prophet(df, target_col='target'):
    prophet_df = df.reset_index()[['date', target_col]].rename(columns={'date': 'ds', target_col: 'y'})
    model = Prophet()
    model.fit(prophet_df)
    forecast = model.predict(prophet_df)
    return forecast['yhat']

# ===== Advanced Models =====
def scenario_based_forecast(data_dict):
    import pandas as pd
    import datetime
    today = datetime.date.today()
    future_dates = [today + datetime.timedelta(days=i) for i in range(30)]
    forecast = [100 + i*2 for i in range(30)]  # Dummy values
    return pd.DataFrame({'date': future_dates, 'forecast': forecast})

