import requests
import json
import tkinter as tk
from tkinter import ttk
import threading
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import sqlite3
from datetime import datetime
import os
matplotlib.use('Agg')

BRIDGE_IP = '192.168.1.100'
USERNAME = 'cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44'
HISTORY_SIZE = 60  # Store 60 seconds of history

# Create data directories if they don't exist
DATA_DIR = "temperature_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Modify the get_hue_temperature_sensors function to print JSON output
def get_hue_temperature_sensors(bridge_ip, username):
    url = f'http://{bridge_ip}/api/{username}/sensors'
    response = requests.get(url)
    
    if response.status_code == 200:
        sensors = response.json()
        temperature_sensors = {}
        for sensor_id, sensor in sensors.items():
            if sensor['type'] == 'ZLLTemperature':
                temperature_sensors[sensor_id] = {
                    'name': sensor['name'],
                    'temperature': sensor['state']['temperature'] / 100.0  # Convert from deci-degrees to degrees Celsius
                }
        print(json.dumps(temperature_sensors), flush=True)  # Only keep this print for Node.js communication
        return temperature_sensors
    else:
        print(json.dumps({}), flush=True)  # Only keep this print for Node.js communication
        return None

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, 'temperature_history.db')
        self.init_database()
        
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS temperature_readings (
                    timestamp DATETIME,
                    sensor_name TEXT,
                    temperature REAL,
                    PRIMARY KEY (timestamp, sensor_name)
                )
            ''')
    
    def save_reading(self, sensor_name, temperature):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO temperature_readings (timestamp, sensor_name, temperature)
                VALUES (?, ?, ?)
            ''', (datetime.now(), sensor_name, temperature))

class TemperatureMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hue Temperature Monitor")
        self.root.geometry("500x400")
        self.root.configure(bg='#2E3440')
        
        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background='#2E3440')
        style.configure("Custom.TLabel",
                       background='#3B4252',
                       foreground='#ECEFF4',
                       padding=10,
                       font=('Helvetica', 12))
        
        self.sensor_frames = {}
        self.sensor_labels = {}
        self.sensor_graphs = {}
        self.temperature_history = {}
        self.running = True
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_temperatures)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.db_manager = DatabaseManager()
        
        # Add status label
        self.status_label = ttk.Label(self.main_frame, 
                                    text="Logging data...", 
                                    style="Custom.TLabel")
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def create_sensor_widgets(self, sensor_name):
        if sensor_name not in self.sensor_frames:
            # Create frame for this sensor
            frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
            frame.pack(fill=tk.X, pady=5)
            
            # Create temperature label
            label = ttk.Label(frame, text=f"{sensor_name}: --°C", 
                            style="Custom.TLabel")
            label.pack(side=tk.LEFT, padx=5)
            
            # Create sparkline
            fig, ax = plt.subplots(figsize=(3, 0.5))
            ax.set_facecolor('#3B4252')
            fig.patch.set_facecolor('#3B4252')
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.RIGHT, padx=5)
            
            # Initialize history
            self.temperature_history[sensor_name] = deque(maxlen=HISTORY_SIZE)
            
            # Store references
            self.sensor_frames[sensor_name] = frame
            self.sensor_labels[sensor_name] = label
            self.sensor_graphs[sensor_name] = (fig, ax, canvas)

    def update_sparkline(self, sensor_name):
        if sensor_name in self.sensor_graphs:
            fig, ax, canvas = self.sensor_graphs[sensor_name]
            history = list(self.temperature_history[sensor_name])
            
            ax.clear()
            if history:
                ax.plot(history, color='#88C0D0', linewidth=1)
                ax.fill_between(range(len(history)), history, 
                              min(history), alpha=0.2, color='#88C0D0')
            
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            fig.tight_layout(pad=0)
            canvas.draw()

    # Modify the update_temperatures method in TemperatureMonitor class
    def update_temperatures(self):
        while self.running:
            sensors = get_hue_temperature_sensors(BRIDGE_IP, USERNAME)
            time.sleep(1)

    def on_closing(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# Remove or comment out the GUI-related code
if __name__ == "__main__":
    while True:
        get_hue_temperature_sensors(BRIDGE_IP, USERNAME)
        time.sleep(1)
