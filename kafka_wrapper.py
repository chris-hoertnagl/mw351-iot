import json
import parser
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps
from parser import parse
import time


class KafkaWrapper:
    BOOTSTRAP_SERVER = "IWILR3-7.CAMPUS.fh-ludwigshafen.de:9092" #"localhost:9092"

    def __init__(self) -> None:
        self.producer = KafkaProducer(bootstrap_servers=self.BOOTSTRAP_SERVER, api_version=(0, 11, 5))

        key_1 = "Power"
        key_2 = "Current"
        key_3 = "Voltage"
        key_4 = "CounterReading"
        self.keys = [key_1, key_2, key_3, key_4]
        self.topic = "EnergyMgmt"

    def kafka_publish(self, data):
        payloads = parser(data)
        # payloads = data
        kafka_dict = {}
        for x in range(len(self.keys)):
            kafka_dict[self.keys[x]] = payloads[x]
        kafka_message = json.dumps(kafka_dict)
        self.producer.send(self.topic, kafka_message.encode())
        print("kafka message sent")


# if __name__ == '__main__':
#     data = ["Hallo", "was", "geht", "ab"]
#     kafka_wrapper = KafkaWrapper()
#     i = 0
    
#     while i < 10:
#         i += 1
#         kafka_wrapper.kafka_publish(data=data)
#         time.sleep(1)
