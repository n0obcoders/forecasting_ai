from .ml_models import (
    run_linear_regression,
    run_arima,
    run_prophet,
    run_moving_average,
    run_exponential_smoothing,
    run_lstm,
    scenario_based_forecast,
)
from .data_cleaning import clean_data
from .utils import calculate_metrics
import pandas as pd
import numpy as np

def detect_seasonality(df, target_col='target'):
    from statsmodels.tsa.stattools import acf
    result = acf(df[target_col], nlags=40, fft=True)
    peaks = np.where(result > 0.5)[0]
    return len(peaks) > 2

def detect_trend(df, target_col='target'):
    from sklearn.linear_model import LinearRegression
    X = np.arange(len(df)).reshape(-1, 1)
    y = df[target_col].values
    model = LinearRegression().fit(X, y)
    return abs(model.coef_[0]) > 0.01

def auto_select_model(df, target_col='target'):
    n = len(df)

    if n == 0:
        return "qualitative"
    if n < 30:
        return "moving_average"

    has_seasonality = detect_seasonality(df, target_col)
    has_trend = detect_trend(df, target_col)
    multivariate = len(df.columns) > 2

    if has_seasonality and has_trend:
        return "prophet"
    elif has_seasonality:
        return "exponential_smoothing"
    elif has_trend and n > 365:
        return "arima"
    elif multivariate:
        return "lstm" if n > 100 else "linear_regression"
    else:
        return "prophet" if n > 100 else "exponential_smoothing"

def forecast(df, model_type="auto", target_col='target'):
    df = clean_data(df)
    
    if model_type == "auto":
        model_type = auto_select_model(df, target_col)

    models = {
        "linear_regression": run_linear_regression,
        "arima": run_arima,
        "prophet": run_prophet,
        "moving_average": run_moving_average,
        "exponential_smoothing": run_exponential_smoothing,
        "lstm": lambda x, y: x  ,
        "qualitative": lambda x, y: scenario_based_forecast({})  # Placeholder
    }

    if model_type not in models:
        raise ValueError(f"Unknown model type: {model_type}")
    
    forecast_df = models[model_type](df, target_col)
    return forecast_df, model_type

def evaluate_models(df, target_col='target', horizon=30):
    results = {}
    train = df.iloc[:-horizon]
    test = df.iloc[-horizon:][target_col]

    for model_name in ["linear_regression", "arima", "prophet",
                       "moving_average", "exponential_smoothing", "lstm"]:
        try:
            forecast_df, _ = forecast(train, model_name, target_col)
            if isinstance(forecast_df, pd.DataFrame):
                pred = forecast_df['forecast']
            elif isinstance(forecast_df, pd.Series):
                pred = forecast_df
            else:
                pred = pd.Series(forecast_df)

            results[model_name] = calculate_metrics(test, pred[:horizon])
        except Exception as e:
            print(f"Error with {model_name}: {e}")
            results[model_name] = {"MAE": None, "RMSE": None}

    return pd.DataFrame(results).T

def run_forecasting_model(df, target_col='target'):
    forecast_df, model_name = forecast(df, model_type="auto", target_col=target_col)

    if isinstance(forecast_df, pd.DataFrame) and 'forecast' in forecast_df.columns:
        predictions = forecast_df['forecast']
    else:
        predictions = forecast_df

    metrics = calculate_metrics(df[target_col], predictions[:len(df)])
    return forecast_df, model_name, metrics
