import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
import io

def fetch_covid_data():
    """Fetch COVID-19 data from NY Times dataset"""
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    response = requests.get(url)
    data = pd.read_csv(io.StringIO(response.text))
    return data

def analyze_covid_data(data):
    """Analyze COVID-19 data and create visualizations"""
    
    data['date'] = pd.to_datetime(data['date'])
    latest_data = data[data['date'] == data['date'].max()].copy()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    top_states = latest_data.nlargest(10, 'cases')
    sns.barplot(data=top_states, x='cases', y='state', ax=ax1)
    ax1.set_title('Top 10 States by Total Cases')
    ax1.set_xlabel('Number of Cases')
    ax1.set_ylabel('State')
    
    
    top_5_states = top_states['state'].tolist()[:5]
    for state in top_5_states:
       
        state_data = data[data['state'] == state].copy()
        state_data['new_cases'] = state_data['cases'].diff()
        ax2.plot(state_data['date'], state_data['new_cases'], label=state)
    
    ax2.set_title('Daily New Cases for Top 5 States')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('New Cases')
    ax2.legend()
    plt.tight_layout()

    plt.savefig('covid_analysis.png')
    plt.close()

def main():
    print("Fetching COVID-19 data...")
    data = fetch_covid_data()
    
    print("Analyzing data and creating visualizations...")
    analyze_covid_data(data)
    
    print("Analysis complete! Check covid_analysis.png for the results.")

if __name__ == "__main__":
    main() 