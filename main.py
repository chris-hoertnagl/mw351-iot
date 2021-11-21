from mqtt_wrapper import MqttWrapper
from kafka_wrapper import KafkaWrapper
import write_db
import time
import subprocess
import datetime
from sml_parser import parse

if __name__ == '__main__':

    # Start smlogger via python subprocess as background process
    CMD = ["smlogger", "-a", "169.254.155.71", "-p", "7259"]
    process = subprocess.Popen(CMD, stdout=subprocess.PIPE)
    print("smlogger subprocess started")

    mqtt_wrapper = MqttWrapper()
    kafka_wrapper = KafkaWrapper()
    print("wrapper ceated")
    
    last_hour = datetime.datetime.now().hour
    
    while True:
        # Read output from smlogger (written to logfile.txt by pylon smlogger)
        with open("logfile.txt", "r") as f:
            data_raw = f.readlines()
        # Publish data via mqtt and kafka client
        if not data_raw:
            print("Empty logfile.txt")
            process.kill()
            process = subprocess.Popen(CMD, stdout=subprocess.PIPE)
            print("smlogger subprocess started")
        else:
            data = parse(data_raw) 
            print("Smart Meter data recieved")
            mqtt_wrapper.mqtt_publish(data)
            try:
                kafka_wrapper.kafka_publish(data)
            except:
                print("Kafka server not running")
            
            # Every hour write value to database
            hour = datetime.datetime.now().hour
            if last_hour != hour:
                print("writing to database")
                write_db.write_to_db(data)
                last_hour = hour
        # Repeat every second
        time.sleep(1)
