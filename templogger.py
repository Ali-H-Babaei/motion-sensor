import requests
import json

# Replace these with your actual Hue Bridge IP address and username
BRIDGE_IP = '192.168.1.100'  # Your Philips Hue Bridge IP address
USERNAME = 'cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44'  # Your newly created username

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
        return temperature_sensors
    else:
        print(f"Failed to connect to the Hue Bridge. Status code: {response.status_code}")
        return None

def main():
    temperature_sensors = get_hue_temperature_sensors(BRIDGE_IP, USERNAME)
    if temperature_sensors:
        print(json.dumps(temperature_sensors, indent=4))
    else:
        print("No temperature sensors found or an error occurred.")

if __name__ == "__main__":
    main()
