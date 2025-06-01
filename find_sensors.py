import requests
import json

hub_ip = "192.168.1.100"
username = "cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44"

try:
    response = requests.get(f'http://{hub_ip}/api/{username}/sensors')
    sensors = response.json()
    
    print("Available Temperature Sensors:")
    print("=" * 50)
    
    for sensor_id, sensor_data in sensors.items():
        # Check if this sensor has temperature data
        if 'temperature' in sensor_data.get('state', {}):
            name = sensor_data.get('name', 'Unknown')
            model = sensor_data.get('modelid', 'Unknown')
            temp = sensor_data.get('state', {}).get('temperature')
            
            print(f"ID: {sensor_id}")
            print(f"  Name: {name}")
            print(f"  Model: {model}")
            print(f"  Current Temperature: {temp}")
            print("-" * 30)
    
    print("\nTo use these sensors, update your sensor string like:")
    temp_sensor_ids = [sensor_id for sensor_id, sensor_data in sensors.items() 
                      if 'temperature' in sensor_data.get('state', {})]
    print(f"sensors = \"{','.join(temp_sensor_ids)}\"")
    
except Exception as e:
    print(f"Error: {e}")