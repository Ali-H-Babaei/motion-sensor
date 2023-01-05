import requests
import threading


class MotionSensor(object):

    def __init__(self, hub_ip: str = None, username: str = None, interval: int = 15, sensor: int = 14):
        self.last_temp = None
        self.hub_ip = hub_ip or None
        self.username = username or None

        if not hub_ip:
            raise ValueError('The hub IP wasn''t provided.')

        if not username:
            raise ValueError('The username wasn''t provided.')

        self.sensor = sensor
        self.interval = interval
        self.temperatures = {}

    def run(self):
        self.check_temp()

    def check_temp(self):
        threading.Timer(int(self.interval), self.check_temp).start()
        response = requests.get(f'http://{self.hub_ip}/api/{self.username}/sensors/{self.sensor}', timeout=60)

        if response.status_code != 200:
            raise ValueError('Unable to get response from motion/temp sensor')

        sensor_state = response.json()

        if not sensor_state['state']['temperature']:
            return -99.99

        temperature = self.get_temp_from_int(sensor_state['state']['temperature'])
        if self.last_temp != temperature:
            print(f'Temp changed! Temp: {temperature:.2f}')
            self.last_temp = temperature
        else:
            print(f'Temp is unchanged. Temp: {temperature:.2f}')
        return temperature

    @staticmethod
    def get_temp_from_int(temp: int = 0):
        # (0°C × 9/5) + 32 = 32°F
        # temp is current temperature in 0.01 degrees Celsius.
        float_val = float(temp/100.0)

        fahrenheit = (float_val * (9 / 5)) + 32.0
        return fahrenheit
