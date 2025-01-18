import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

DATA_DIR = "temperature_data"
DB_PATH = os.path.join(DATA_DIR, 'temperature_history.db')

def get_temperature_data(days=1, sensor_name=None):
    """
    Get temperature readings for the specified number of days
    Args:
        days: Number of days of history to retrieve
        sensor_name: Optional sensor name filter
    """
    query = """
        SELECT timestamp, sensor_name, temperature
        FROM temperature_readings
        WHERE timestamp > datetime('now', ?)
    """
    params = [f'-{days} days']
    
    if sensor_name:
        query += " AND sensor_name = ?"
        params.append(sensor_name)
    
    query += " ORDER BY timestamp"
    
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params, 
                               parse_dates=['timestamp'])

def plot_temperature_history(days=1):
    """Plot temperature history for all sensors"""
    df = get_temperature_data(days=days)
    
    plt.figure(figsize=(12, 6))
    for sensor in df['sensor_name'].unique():
        sensor_data = df[df['sensor_name'] == sensor]
        plt.plot(sensor_data['timestamp'], 
                sensor_data['temperature'], 
                label=sensor)
    
    plt.title(f'Temperature History - Last {days} Days')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    plt.show()

def get_stats(days=1):
    """Get temperature statistics for all sensors"""
    df = get_temperature_data(days=days)
    return df.groupby('sensor_name').agg({
        'temperature': ['min', 'max', 'mean', 'std']
    }).round(2)

if __name__ == "__main__":
    # Example usage:
    print("\nTemperature Statistics (Last 24 hours):")
    print(get_stats(days=1))
    
    print("\nPlotting temperature history...")
    plot_temperature_history(days=1)
    
    # Example of custom query
    print("\nLast 5 readings:")
    df = get_temperature_data(days=1)
    print(df.tail())
