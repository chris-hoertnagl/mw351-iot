import paho.mqtt.client as paho
from sml_parser import parse
import json


class MqttWrapper():
    BROKER = "IWILR3-6.CAMPUS.fh-ludwigshafen.de"
    PORT = 1883
    CLIENT_NAME = "Bret"

    def __init__(self):
        self.client = paho.Client(self.CLIENT_NAME)
        self.client.connect(self.BROKER, self.PORT)

        topic_1 = "EnergyMgmt/SM000001/Power"
        topic_2 = "EnergyMgmt/SM000001/Current"
        topic_3 = "EnergyMgmt/SM000001/Voltage"
        topic_4 = "EnergyMgmt/SM000001/CounterReading"
        self.topics = [topic_1, topic_2, topic_3, topic_4]

    def mqtt_publish(self, data):
        # Parse Smart Meter output into topics
        payloads = parse(data)
        print("publishing mqtt topics")
        # Publish topics
        for x in range(len(self.topics)):
            try:
                self.client.publish(self.topics[x], json.dumps(
                    payloads[x]), qos=0, retain=False)
            except:
                print("Failed publishing message")
