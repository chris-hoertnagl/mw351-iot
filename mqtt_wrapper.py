import paho.mqtt.client as paho
from sml_parser import parse
import json


class MqttWrapper():
    BROKER = "IWILR3-7.CAMPUS.fh-ludwigshafen.de"
    PORT = 1883
    CLIENT_NAME = "Bret"

    def __init__(self):
        self.client = paho.Client(self.CLIENT_NAME)
        self.client.connect(self.BROKER, self.PORT)

        topic_1 = "Smarthome/EnergyMgmt/SM000001/Power"
        topic_2 = "Smarthome/EnergyMgmt/SM000001/Current"
        topic_3 = "Smarthome/EnergyMgmt/SM000001/Voltage"
        topic_4 = "Smarthome/EnergyMgmt/SM000001/CounterReading"
        topic_5 = "Smarthome/EnergyMgmt/SM000001/Consumption"
        self.topics = [topic_1, topic_2, topic_3, topic_4, topic_5]

    def mqtt_publish(self, data):
        # Parse Smart Meter output into topics
        payloads = data
        # Publish topics
        for x in range(len(self.topics)):
            try:
                self.client.publish(self.topics[x], json.dumps(
                    payloads[x]), qos=0, retain=False)
                print(f"published {payloads[x]} to {self.topics[x]}")
            except:
                print("Failed publishing message")
