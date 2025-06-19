import pandas as pd
import streamlit as st

class QualitativeForecaster:
    def __init__(self):
        self.experts = {}
        self.scenarios = {
            'Best-case': 1.0,
            'Most-likely': 1.0,
            'Worst-case': 1.0
        }
        self.confidence_scores = {}
    
    def delphi_round(self, expert_name, forecast_value, confidence):
        """Record expert input with confidence scoring"""
        self.experts[expert_name] = forecast_value
        self.confidence_scores[expert_name] = confidence
        
        # Calculate weighted average
        weights = [self.confidence_scores[e] for e in self.experts]
        values = [self.experts[e] for e in self.experts]
        weighted_avg = np.average(values, weights=weights)
        
        return weighted_avg
    
    def scenario_forecast(self, base_value):
        """Generate scenario-based forecasts"""
        return {
            'Best-case': base_value * self.scenarios['Best-case'],
            'Most-likely': base_value * self.scenarios['Most-likely'],
            'Worst-case': base_value * self.scenarios['Worst-case']
        }
    
    def run_delphi_process(self, rounds=3):
        """Simulate multi-round Delphi method"""
        st.sidebar.header("Delphi Method Configuration")
        num_experts = st.sidebar.number_input("Number of Experts", 3, 10, 5)
        
        results = []
        for round_num in range(1, rounds+1):
            st.subheader(f"Round {round_num}/{rounds}")
            round_results = {}
            
            for i in range(num_experts):
                col1, col2 = st.columns(2)
                with col1:
                    forecast = st.number_input(f"Expert {i+1} Forecast", 
                                             key=f"expert_{i}_round_{round_num}")
                with col2:
                    confidence = st.slider(f"Confidence (0-100)", 0, 100, 75,
                                          key=f"conf_{i}_round_{round_num}")
                round_results[f"Expert {i+1}"] = (forecast, confidence/100)
            
            # Store results
            results.append(round_results)
            
            # Show summary
            values = [v[0] for v in round_results.values()]
            confidences = [v[1] for v in round_results.values()]
            weighted_avg = np.average(values, weights=confidences)
            
            st.metric(f"Round {round_num} Weighted Average", f"{weighted_avg:.2f}")
        
        return results

def scenario_based_forecast(base_value):
    forecaster = QualitativeForecaster()
    
    st.sidebar.header("Scenario Parameters")
    forecaster.scenarios['Best-case'] = st.sidebar.slider("Best-case Multiplier", 
                                                         0.5, 2.0, 1.2)
    forecaster.scenarios['Most-likely'] = st.sidebar.slider("Most-likely Multiplier", 
                                                           0.5, 2.0, 1.0)
    forecaster.scenarios['Worst-case'] = st.sidebar.slider("Worst-case Multiplier", 
                                                          0.5, 2.0, 0.8)
    
    return forecaster.scenario_forecast(base_value)
