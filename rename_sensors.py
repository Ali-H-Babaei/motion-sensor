import requests
import json

# Replace these with your actual Hue Bridge IP address and username
BRIDGE_IP = '192.168.1.100'  # Your Philips Hue Bridge IP address
USERNAME = 'cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44'  # Your Hue username

# List of sensor IDs and their new names
sensors_to_rename = [
    {'id': '4', 'new_name': 'Porch Temperature Sensor'},
    {'id': '23', 'new_name': 'Office Temperature Sensor'},
    {'id': '28', 'new_name': 'Kitchen Hallway Temperature Sensor'},
    {'id': '63', 'new_name': 'Wardrobe Temperature Sensor'},
    {'id': '82', 'new_name': 'Kitchen Temperature Sensor'},
    {'id': '95', 'new_name': 'Bathroom Temperature Sensor'},
    {'id': '104', 'new_name': 'Ensuite Temperature Sensor'}
]

def rename_sensor(bridge_ip, username, sensor_id, new_name):
    url = f'http://{bridge_ip}/api/{username}/sensors/{sensor_id}'
    data = json.dumps({"name": new_name})
    response = requests.put(url, data=data)
    
    if response.status_code == 200:
        print(f"Sensor {sensor_id} renamed to {new_name}.")
    else:
        print(f"Failed to rename sensor {sensor_id}. Status code: {response.status_code}, Response: {response.text}")

def main():
    for sensor in sensors_to_rename:
        sensor_id = sensor['id']
        new_name = sensor['new_name']
        rename_sensor(BRIDGE_IP, USERNAME, sensor_id, new_name)

if __name__ == "__main__":
    main()
