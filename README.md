# earnapp2mqtt
A MQTT Docker to connect to the Earnapp

Using the earnapp Python package and the paho.mqtt Python package, this application retrieves the information from your Earnapp dashboard and publishes it via MQTT

## Environment Variables
```
MQTT_IP: The IP of your MQTT Broker
MQTT_PORT: The port of your MQTT Broker
MQTT_USER: The username for your MQTT Broker
MQTT_PASS: The password for your MQTT Broker
USER_TOKEN: Your OAuth Refresh Token for the Earnapp dashboard (can't be retrieved by inspecting the request made on the dashboard webapp)
```
