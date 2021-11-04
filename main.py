from mqtt_wrapper import MqttWrapper
from kafka_wrapper import KafkaWrapper
import write_db
import time
import subprocess

if __name__ == '__main__':

    # Start smlogger via python subprocess as background process
    CMD = ["smlogger", "-a", "169.254.155.71", "-p", "7259"]
    process = subprocess.Popen(CMD, stdout=subprocess.PIPE)
    print("smlogger subprocess started")

    mqtt_wrapper = MqttWrapper()
    kafka_wrapper = KafkaWrapper()
    print("mqtt wrapper ceated")
    while True:
        # Read output from smlogger (written to logfile.txt by pylon smlogger)
        with open("logfile.txt", "r") as f:
            data = f.readlines()
        # Publish data via mqtt and kafka client
        if not data:
            print("Empty logfile.txt")
            process = subprocess.Popen(CMD, stdout=subprocess.PIPE)
            print("smlogger subprocess started")
        else:
            print("Smart Meter data recieved")
            mqtt_wrapper.mqtt_publish(data)
            kafka_wrapper.kafka_publish(data)
            #write_db.write_to_db(data)
        # Repeat every second
        time.sleep(1)
