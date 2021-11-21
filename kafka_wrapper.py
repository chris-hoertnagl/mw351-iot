import json
from kafka import KafkaProducer
from json import dumps
from sml_parser import parse

class KafkaWrapper:
    BOOTSTRAP_SERVER = "IWILR3-7.CAMPUS.fh-ludwigshafen.de:9092"

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=self.BOOTSTRAP_SERVER, api_version=(0, 11, 5), max_block_ms=1000)

        key_1 = "Power"
        key_2 = "Current"
        key_3 = "Voltage"
        key_4 = "CounterReading"
        key_5 = "Consumption"
        self.keys = [key_1, key_2, key_3, key_4, key_5]
        self.topic = "EnergyMgmt"

    def kafka_publish(self, data):
        payloads = data
        kafka_dict = {}
        for x in range(len(self.keys)):
            try:
                    kafka_dict[self.keys[x]] = payloads[x]
            except:
                    pass
        kafka_message = json.dumps(kafka_dict)
        self.producer.send(self.topic, kafka_message.encode())
        print("kafka message sent")
