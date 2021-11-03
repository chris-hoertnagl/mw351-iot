import paho.mqtt.client as paho
from parser import parse


class MqttWrapper():
    BROKER = "IWILR3-6.CAMPUS.fh-ludwigshafen.de"
    PORT = 1883
    CLIENT_NAME = "Bret"

    def __init__(self) -> None:
        self.client = paho.Client(self.CLIENT_NAME)
        self.client.connect(self.BROKER, self.PORT)

        topic_1 = "EnergyMgmt/SM000001/Power"
        topic_2 = "EnergyMgmt/SM000001/Current"
        topic_3 = "EnergyMgmt/SM000001/Voltage"
        topic_4 = "EnergyMgmt/SM000001/CounterReading"
        self.topics = [topic_1, topic_2, topic_3, topic_4]

    def mqtt_publish(self, data):
        if data != None:
            # Parse Smart Meter output into topics
            payloads = parse(data)

            # Publish topics
            for x in range(len(self.topics)):
                self.client.publish(
                    self.topics[x], payloads[x], qos=0, retain=False)
