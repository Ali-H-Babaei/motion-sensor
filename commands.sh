

192.168.1.100 alan.babaei@outlook.com cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44
 
python3 main.py -b $HUE_BRIDGE_IP -u $HUE_USERNAME -s 5,18 -i 10

python3 main.py -b 192.168.1.100 -u curl http://192.168.1.100/api/cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44/sensors -s 5,18 -i 10

curl http://192.168.1.100/api/cwdsZSo7ZvSxxoNBS9funK2QfizEyRG3MdABw-44/sensors


curl https://192.168.1.100/clip/v2/resource/device


curl -X POST -d '{"devicetype":"my_hue_app"}' http://192.168.1.100/api
