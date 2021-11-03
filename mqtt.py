import paho.mqtt.client as paho
from parser import parse


def mqtt_publish(data):
    broker = "IWILR3-6.CAMPUS.fh-ludwigshafen.de"
    port = 1883

    if data != None:
        # Parse Smart Meter output into topics
        topics, payloads = parse(data)
        bret_client = paho.Client("Bret")
        bret_client.connect(broker, port)
        # Publish topics
        for x in range(len(topics)):
            bret_client.publish(topics[x], payloads[x], qos=0, retain=False)
