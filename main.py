import json
from pprint import pprint
from earnapp import earnapp
from os import getenv
from time import sleep
import logging
import paho.mqtt.client

version = "1.3.0"
FORMAT = ('%(asctime)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        log.info("MQTT OK!")
    else:
        log.info("MQTT FAILURE. ERROR CODE: %s", rc)


def connect_to_mqtt():
    mqtt_host = getenv('MQTT_IP', '192.168.1.1')
    mqtt_port = int(getenv('MQTT_PORT', '1883'))

    paho.mqtt.client.Client.connected_flag = False  # create flag in class
    clientMQTT = paho.mqtt.client.Client()

    clientMQTT.on_connect = on_connect  # bind call back function
    clientMQTT.loop_start()

    log.info("Connecting to MQTT broker: %s:%d ", mqtt_host, mqtt_port)

    clientMQTT.username_pw_set(username=getenv('MQTT_USER', 'user'),
                               password=getenv('MQTT_PASS', 'password'))
    clientMQTT.connect(mqtt_host, mqtt_port)  # connect to broker

    return clientMQTT


clientMQTT = connect_to_mqtt()
while not clientMQTT.connected_flag:  # wait in loop
    # log.info("...")
    pass
sleep(1)

try:
    user = earnapp.User()
    user.login(getenv("USER_TOKEN"))
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise SystemExit

while True:
    devices = user.devices()
    money = user.money()

    clientMQTT.publish(topic="earnapp/devices",
                       payload=json.dumps(devices), qos=1, retain=False)
    log.info('🚀 Published device information...')

    clientMQTT.publish(topic="earnapp/money",
                       payload=json.dumps(money), qos=1, retain=False)
    log.info('🚀 Published money information...')

    sleep(30)
