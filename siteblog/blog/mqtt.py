import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("temperature")

    # The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set(
    '5JUzKDJlbJg75q5PhQ0B4PyFnFr1ZvHT4qiCTPOSnSPi6KVdqKCip1NDu2uklZ3d', '')
client.connect("ru-mqtt.flespi.io", 1883)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
