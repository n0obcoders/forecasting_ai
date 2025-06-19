import unittest
from forecasting_engine import forecast
import pandas as pd

class TestForecasting(unittest.TestCase):
    def test_arima_forecast(self):
        test_data = pd.DataFrame({
            'date': pd.date_range(start='2020-01-01', periods=100),
            'target': range(100)
        })
        result = forecast(test_data, model_type='arima')
        self.assertEqual(len(result), 30)
    
    # Add tests for other models

if __name__ == '__main__':
    unittest.main()
