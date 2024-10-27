import requests
import random
import pandas as pd
import time
import csv
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import os
import warnings
from datetime import datetime, timedelta

API_KEY = None
API_ENDPOINT = None
NUM_TEST_ROWS = 2000

def get_olympics_data_from_api(api_key, api_endpoint):
    try:
        response = requests.get(api_endpoint, headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Error occurred: {err}")
        return None

def clean_olympics_data(data):
    sports_data_list = [
        {
            'Timestamp': entry['Timestamp'],
            'Viewer IPs': entry['ip_address'],
            'User ID': entry['user_id'],
            'Country': entry['country'],
            'Sport': entry['sport'],
            'Duration': entry['duration'],
            'Device': entry['device'],
            'Channel': entry['channel']
        } for entry in data
    ]

    sports_data_df = pd.DataFrame(sports_data_list)
    sports_data_df.replace('', pd.NA, inplace=True)
    sports_data_df.dropna(inplace=True)
    return sports_data_df

def generate_random_ip_addresses(num_addresses):
    return ['.'.join(str(random.choice(range(1, 255))) for _ in range(4)) for _ in range(num_addresses)]

def generate_timestamps(start_date, end_date):
    timestamps = []
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            timestamps.append(current_date.strftime(f'%Y-%m-%d {hour:02}:00:00'))
        current_date += datetime.timedelta(days=1)
    return timestamps


import datetime
START_DATE = datetime.date(2024, 7, 6)
END_DATE = datetime.date(2024, 7, 10)

def generate_test_data(num_rows):
    random_ip_addresses = generate_random_ip_addresses(num_rows)
    timestamps = generate_timestamps(START_DATE, END_DATE)
    user_ids = list(range(10000, 20000))
    countries = ['USA', 'Canada', 'Mexico', 'Chile', 'Brazil', 'Namibia', 'South Africa']
    sports = ['Swimming', 'Basketball', 'Soccer', 'Hockey', 'Snowboarding', 'Tennis']
    durations = [30, 60, 90, 40, 50, 10, 120, 70, 80]
    devices = ['Desktop', 'Mobile', 'Tablet']
    channels = ['Main Channel', 'Events Channel 2', 'Live Sports']

    sports_data = []
    for _ in range(num_rows):
        sports_data.append({
            'Timestamp': pd.to_datetime(random.choice(timestamps)),
            'Viewer IPs': random.choice(random_ip_addresses),
            'User ID': random.choice(user_ids),
            'Country': random.choice(countries),
            'Sport': random.choice(sports),
            'Duration': random.choice(durations),
            'Device': random.choice(devices),
            'Channel': random.choice(channels)
        })
    return pd.DataFrame(sports_data)

def get_data(use_api=False, api_key=None, api_endpoint=None):
    if use_api:
        if api_key and api_endpoint:
            time.sleep(15)  # Add a 15-second sleep
            data = get_olympics_data_from_api(api_key, api_endpoint)
            if data:
                fun_olympics_df = clean_olympics_data(data)
                return fun_olympics_df
        else:
            print("API key or endpoint not provided. Returning generated data instead.")
    else:
        fun_olympics_test = generate_test_data(NUM_TEST_ROWS)
        return fun_olympics_test

df = pd.read_csv("olympics_data.csv")

# Ensure correct data types
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Country"] = df["Country"].astype(str)
df["Sport"] = df["Sport"].astype(str)
df["Device"] = df["Device"].astype(str)

# Page configuration
st.set_page_config(page_title="FunOlympics_Dash", page_icon=":bar_chart:", layout="wide")
st.title("Fun Olympics Streaming Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Choose your filter:")
Country = st.sidebar.multiselect("Pick your Country", df["Country"].unique())
Sport = st.sidebar.multiselect("Pick the Sport", df["Sport"].unique())
Device = st.sidebar.multiselect("Pick the Device", df["Device"].unique())

# Filter data based on sidebar input
def filter_data(df, Country, Sport, Device):
    if Country:
        df = df[df["Country"].isin(Country)]
    if Sport:
        df = df[df["Sport"].isin(Sport)]
    if Device:
        df = df[df["Device"].isin(Device)]
    return df

# Chart functions
def create_views_per_sport_chart(df):
    category_df = df.groupby(by=["Sport"], as_index=False)["Duration"].sum()
    fig = px.bar(category_df, x="Sport", y="Duration", text=['{:,d}'.format(x) for x in category_df["Duration"]],
                 template="seaborn")
    fig.update_layout(title_text = "Views Per Sport")
    return fig

def create_views_per_country_chart(df):
    fig = px.pie(df, values="Duration", names="Country", hole=0.5)
    fig.update_traces(text=df["Country"], textposition="outside")
    fig.update_layout(title_text = "Views Per Country")
    return fig

def create_time_series_chart(df):
    df["date"] = df["Timestamp"].dt.date
    linechart = pd.DataFrame(df.groupby(df["date"])["Duration"].sum()).reset_index()
    fig = px.line(linechart, x="date", y="Duration", labels={"Duration": "Views"}, height=500, width=1000, template="gridon")
    fig.update_layout(title_text = "Time Series Chart")
    return fig

def create_views_by_channel_chart(df):
    fig = px.pie(df, values="Duration", names="Channel", template="plotly_dark")
    fig.update_traces(text=df["Channel"], textposition="inside")
    fig.update_layout(title_text = "Views Per Channel")
    return fig

def create_views_by_device_chart(df):
    fig = px.pie(df, values="Duration", names="Device", template="gridon")
    fig.update_traces(text=df["Device"], textposition="inside")
    fig.update_layout(title_text = "Views Per Device")
    return fig

def create_summary_table(df):
    df_sample = df[0:15][['Timestamp', 'Country', 'Duration', 'Sport', 'Device', 'Channel']]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    fig.update_layout(title_text="Summary Table")
    return fig

# Dashboard layout with placeholders
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
views_per_sport_placeholder = col1.empty()
views_per_country_placeholder = col2.empty()
views_by_channel_placeholder = col3.empty()
views_by_device_placeholder = col4.empty()
time_series_placeholder = st.empty()
summary_table_placeholder = st.empty()

st.download_button(label="Download data as CSV", data=df.to_csv(index=False).encode('utf-8'),file_name='filtered_data.csv', mime='text/csv')

# Simulate real-time updates
while True:
    df = get_data(use_api=False)  # Fetch new data
    df = filter_data(df, Country, Sport, Device)  # Apply filters
    
    with views_per_sport_placeholder:
        fig = create_views_per_sport_chart(df)
        st.plotly_chart(fig, use_container_width=True)

    with views_per_country_placeholder:
        fig = create_views_per_country_chart(df)
        st.plotly_chart(fig, use_container_width=True)

    with time_series_placeholder:
        fig = create_time_series_chart(df)
        st.plotly_chart(fig, use_container_width=True)

    with views_by_channel_placeholder:
        fig = create_views_by_channel_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with views_by_device_placeholder:
        fig = create_views_by_device_chart(df)
        st.plotly_chart(fig, use_container_width=True)

    summary_table  = create_summary_table(df)
    summary_table_placeholder.plotly_chart(summary_table, use_container_width= True)
    
    time.sleep(3)  # Update every 3 seconds
