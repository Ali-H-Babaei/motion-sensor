# motion-sensor

Python example using the Philips Hue API and the Philips Hue motion sensor. The motion sensor this is using has temperature information in celcius available in the sensor's state information.

The Philips Hue API doesn't list "temperature" as an available state value so here is additional information regarding the sensor being used in case not all Philips Hue motion sensors have temperature available:

| Property          | Value                    |
|:------------------|:-------------------------|
| Type              | ZLLTemperature           |
| Model id          | SML001                   |
| Manufacturer Name | Signify Netherlands B.V. |
| Product Name      | Hue temperature sensor   |
| Software Version  | 6.1.1.27575              | 

## Command Line Args

| Short Option | Long Option | Description |
|:---:|:---:|:---|
| `-b` |  `--bridge` | Bridge, or hub, IP address |
| `-u` | `--username` |  Username created for interacting with the Hue Bridge |
| `-i` | `--interval` |  Interval in seconds to check motion sensor temperature value |
| `-s` |`--sensor` | Sensor id for the sensor to monitor |

