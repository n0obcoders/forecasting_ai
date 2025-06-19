from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def calculate_metrics(actual, predicted):
    """Calculate MAE and RMSE with alignment handling"""
    # Align series
    actual, predicted = align_series(actual, predicted)
    
    if len(actual) == 0:
        return {"MAE": None, "RMSE": None}
    
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return {'MAE': mae, 'RMSE': rmse}

def align_series(actual, predicted):
    """Align two series by index"""
    if isinstance(actual, pd.Series) and isinstance(predicted, pd.Series):
        common_index = actual.index.intersection(predicted.index)
        return actual.loc[common_index], predicted.loc[common_index]
    return actual, predicted

def compare_models(results_df):
    """Highlight best model in evaluation results"""
    if results_df.empty:
        return results_df
    
    # Find best model for each metric
    best_mae = results_df['MAE'].idxmin()
    best_rmse = results_df['RMSE'].idxmin()
    
    # Create styled DataFrame
    styled_df = results_df.style.highlight_min(subset=['MAE'], color='lightgreen')
    styled_df = styled_df.highlight_min(subset=['RMSE'], color='lightblue')
    
    # Add annotations
    styled_df = styled_df.set_caption(
        f"Best MAE: {best_mae} | Best RMSE: {best_rmse}")
    
    return styled_df
