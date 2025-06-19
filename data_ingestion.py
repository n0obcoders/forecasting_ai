import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import yfinance as yf
import os
from datetime import datetime

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def get_random_agent():
    return random.choice(USER_AGENTS)

def safe_request(url, max_retries=3):
    for _ in range(max_retries):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": get_random_agent()},
                timeout=15
            )
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Retry {_+1}/{max_retries} for {url}: {e}")
            time.sleep(2 + random.random()*3)
    return None

# ================== File Data Loading ==================
def load_file_data(file_path):
    """Auto-detect and load data file with validation"""
    # Detect file type
    ext = os.path.splitext(file_path)[1].lower()
    
    # Read file
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext == '.xlsx' or ext == '.xls':
        df = pd.read_excel(file_path)
    elif ext == '.json':
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Validate structure
    validate_data_structure(df)
    
    return df

def validate_data_structure(df):
    """Ensure data has required columns"""
    required_columns = {'date', 'revenue', 'sales', 'expenses', 
                       'profit', 'cashflow', 'demand'}
    found_columns = set(df.columns)
    
    # Check for date column
    if 'date' not in found_columns:
        raise ValueError("Data must contain 'date' column")
    
    # Check for at least one financial metric
    if len(found_columns.intersection(required_columns)) < 1:
        raise ValueError("Data must contain at least one financial metric column")
    
    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return True

# ================== MoneyControl ================== 
def get_moneycontrol_sc_id(ticker: str):
    url = f"https://www.moneycontrol.com/mc/mccommon/suggestions?query={ticker}&type=1&format=json"
    response = safe_request(url)
    if response:
        try:
            suggestions = response.json()
            if suggestions and 'suggestions' in suggestions:
                return suggestions['suggestions'][0]['sc_id']
        except:
            pass
    return None

def fetch_moneycontrol_financials(ticker: str, statement_type: str = 'income'):
    sc_id = get_moneycontrol_sc_id(ticker)
    if not sc_id:
        return None
        
    url = f"https://www.moneycontrol.com/mc/widget/getdetailedfinancial?classic=true&scId={sc_id}&type={statement_type}"
    response = safe_request(url)
    if response:
        try:
            data = response.json()
            return pd.DataFrame(data['data'])
        except:
            pass
    return None

# ================== Motilal Oswal ==================
def fetch_motilal_oswal_research(ticker: str):
    url = f"https://www.motilaloswal.com/api/research/reports?symbol={ticker}"
    response = safe_request(url)
    if response:
        try:
            reports = response.json()['data']
            return pd.DataFrame(reports)[['reportDate', 'title', 'pdfLink']]
        except:
            pass
    return None

# ================== Trendlyne ==================
def fetch_trendlyne_insights(ticker: str):
    url = f"https://trendlyne.com/equity/{ticker}/"
    response = safe_request(url)
    if response:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            insights = []
            for card in soup.select('.card-body'):
                title = card.select_one('.card-title')
                value = card.select_one('.card-text')
                if title and value:
                    insights.append({
                        "metric": title.text.strip(),
                        "value": value.text.strip()
                    })
            return pd.DataFrame(insights)
        except:
            pass
    return None

# ================== ICICI Direct ==================
def fetch_icici_direct_analysis(ticker: str):
    url = f"https://www.icicidirect.com/equity/{ticker}"
    response = safe_request(url)
    if response:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            analysis = {}
            for div in soup.select('.key-metrics li'):
                parts = div.text.split(':')
                if len(parts) > 1:
                    analysis[parts[0].strip()] = parts[1].strip()
            return pd.DataFrame([analysis])
        except:
            pass
    return None

# ================== Corporate Finance Institute ==================
def fetch_cfi_resources(topic: str):
    url = f"https://corporatefinanceinstitute.com/resources/search/?q={topic}"
    response = safe_request(url)
    if response:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            resources = []
            for card in soup.select('.post-card'):
                title = card.select_one('.post-card__title')
                link = card.select_one('a')['href']
                if title and link:
                    resources.append({
                        "title": title.text.strip(),
                        "url": "https://corporatefinanceinstitute.com" + link
                    })
            return pd.DataFrame(resources)
        except:
            pass
    return None

# ================== IIFL (India Infoline Limited) ==================
def fetch_iifl_news(ticker: str):
    url = f"https://www.indiainfoline.com/company/{ticker.lower()}/news-and-research/378"
    response = safe_request(url)
    if response:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            for item in soup.select('.news-listing li'):
                headline = item.select_one('a')
                date = item.select_one('.date')
                if headline and date:
                    news_items.append({
                        "headline": headline.text.strip(),
                        "date": date.text.strip(),
                        "url": "https://www.indiainfoline.com" + headline['href']
                    })
            return pd.DataFrame(news_items)
        except Exception as e:
            print(f"IIFL parsing error: {e}")
    return None

# ================== Bloomberg (Placeholder) ==================
def fetch_bloomberg_data(ticker: str, data_type: str = 'quote'):
    print(f"Fetching {data_type} for {ticker} from Bloomberg...")
    return pd.DataFrame()

# ================== Unified Data Loader ==================
def load_data(source: str, **kwargs):
    """
    Unified data loader with support for:
    - Web sources: moneycontrol, motilaloswal, trendlyne, icicidirect, cfi, iifl, bloomberg, yahoo
    - File sources: csv, excel, json
    
    Parameters:
    source: Data source identifier
    **kwargs: Source-specific parameters:
        For files: file_path
        For web: ticker, data_type, period, etc.
    """
    # File-based sources
    if source in ['csv', 'excel', 'json']:
        return load_file_data(kwargs['file_path'])
    
    # Web-based sources
    ticker = kwargs.get('ticker', '')
    data_type = kwargs.get('data_type', 'financials')
    
    if source == 'moneycontrol':
        if data_type == 'financials':
            return fetch_moneycontrol_financials(
                ticker, 
                kwargs.get('statement_type', 'income')
            )
    
    elif source == 'motilaloswal':
        return fetch_motilal_oswal_research(ticker)
    
    elif source == 'trendlyne':
        return fetch_trendlyne_insights(ticker)
    
    elif source == 'icicidirect':
        return fetch_icici_direct_analysis(ticker)
    
    elif source == 'cfi':
        return fetch_cfi_resources(kwargs.get('topic', 'valuation'))
    
    elif source == 'iifl':
        return fetch_iifl_news(ticker)
    
    elif source == 'bloomberg':
        return fetch_bloomberg_data(ticker, data_type)
    
    elif source == 'yahoo':
        stock = yf.Ticker(ticker)
        if data_type == 'history':
            return stock.history(period=kwargs.get('period', '1y'))
        elif data_type == 'financials':
            return stock.income_stmt
    
    raise ValueError(f"Unsupported source: {source}")

# ================== Sample Data Generator ==================
def generate_sample_data():
    """Create sample financial data template"""
    dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
    return pd.DataFrame({
        'date': dates,
        'revenue': [10000, 12000, 15000, 13000, 14000, 16000, 
                   17000, 18000, 19000, 20000, 22000, 25000],
        'expenses': [6000, 6500, 7000, 6800, 7200, 7500, 
                    8000, 8500, 9000, 9500, 10000, 11000],
        'profit': [4000, 5500, 8000, 6200, 6800, 8500, 
                  9000, 9500, 10000, 10500, 12000, 14000],
        'cashflow': [2000, 2500, 3000, 2800, 3200, 3500, 
                    4000, 4200, 4500, 4800, 5000, 5500],
        'demand': [500, 550, 600, 580, 620, 650, 
                  700, 720, 750, 780, 800, 850]
    })

# ================== Main Function (Test) ==================
if __name__ == "__main__":
    # Example usage
    print("Sample Data Template:")
    print(generate_sample_data().head())
    
    print("\nLoading sample CSV data:")
    sample_df = generate_sample_data()
    sample_df.to_csv("sample_financial_data.csv", index=False)
    print(load_data('csv', file_path="sample_financial_data.csv").head())
