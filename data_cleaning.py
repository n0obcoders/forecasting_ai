import pandas as pd

def clean_data(df: pd.DataFrame):
    # Handle missing values
    df = df.interpolate(method='time').fillna(method='bfill')
    
    # Convert date column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    
    # Normalize numerical columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    
    return df
