import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
import io
import base64

app = Flask(__name__)

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
    
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url, top_states.to_dict('records')

@app.route('/')
def index():
    
    data = fetch_covid_data()
    plot_url, top_states = analyze_covid_data(data)
    
    
    latest_date = data['date'].max().strftime('%B %d, %Y')
    total_cases = data[data['date'] == data['date'].max()]['cases'].sum()
    total_deaths = data[data['date'] == data['date'].max()]['deaths'].sum()
    
    return render_template('index.html',
                         plot_url=plot_url,
                         top_states=top_states,
                         latest_date=latest_date,
                         total_cases=total_cases,
                         total_deaths=total_deaths)

if __name__ == '__main__':
    app.run(debug=True) 