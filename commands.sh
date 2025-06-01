

192.168.1.100 alan.babaei@outlook.com cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44
 
python3 main.py -b $HUE_BRIDGE_IP -u $HUE_USERNAME -s 5,18 -i 10

python3 main.py -b 192.168.1.100 -u curl http://192.168.1.100/api/cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44/sensors -s 5,18 -i 10

curl http://192.168.1.100/api/cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44/sensors


curl https://192.168.1.100/clip/v2/resource/device


curl -X POST -d '{"devicetype":"my_hue_app"}' http://192.168.1.100/api

# to find and then update the temperature sensor name
$response = Invoke-RestMethod "http://192.168.1.100/api/cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44/sensors"
$response.PSObject.Properties | 
Where-Object { $_.Value.type -eq "ZLLTemperature" } | 
Select-Object @{N='ID';E={$_.Name}}, 
              @{N='Name';E={$_.Value.name}}, 
              @{N='Type';E={$_.Value.type}},
              @{N='Temperature';E={[math]::Round($_.Value.state.temperature/100,2)}} |
Format-Table