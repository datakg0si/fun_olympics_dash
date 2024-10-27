# FunOlympics_Dash : A Streamlit Dashboard Scenario

## Overview

**FunOlympics_Dash** is a Streamlit-based interactive dashboard for visualizing and analyzing streaming data from the Fun Olympics. The dashboard provides real-time insights into various metrics such as views per sport, views per country, views by device, and more. It also supports filtering data based on country, sport, and device, allowing for customized and detailed analysis.

## Features

- **Interactive Filters**: Filter data by country, sport, and device through the sidebar.
- **Real-time Updates**: The dashboard updates every 3 seconds to reflect the latest data.
- **Data Visualization**: Various charts and plots including bar charts, pie charts, line charts, and summary tables.
- **CSV Download**: Download the filtered data as a CSV file.

## Data

The dashboard can fetch data from two sources:

1. **API Data**: If you have an API key and endpoint, you can configure the dashboard to fetch real-time data from an API.
2. **Generated Data**: For testing purposes, the dashboard can generate random data.

### Data Columns

- **Timestamp**: The timestamp of the viewing event.
- **Viewer IPs**: The IP address of the viewer.
- **User ID**: The ID of the user.
- **Country**: The country of the viewer.
- **Sport**: The sport being viewed.
- **Duration**: The duration of the viewing event.
- **Device**: The device used to view the content.
- **Channel**: The channel on which the content was viewed.

## Usage

### Filtering Data

Use the sidebar to filter the data by country, sport, and device. The dashboard will update automatically to reflect the selected filters.

### Visualizations

- **Views Per Sport**: Bar chart showing the total viewing duration per sport.
- **Views Per Country**: Pie chart showing the distribution of viewing duration by country.
- **Time Series Chart**: Line chart showing the total viewing duration over time.
- **Views Per Channel**: Pie chart showing the distribution of viewing duration by channel.
- **Views Per Device**: Pie chart showing the distribution of viewing duration by device.
- **Summary Table**: A table summarizing the first 15 rows of the filtered data.

### Download Data

Click the "Download data as CSV" button to download the filtered data in CSV format.
