from mqtt_wrapper import MqttWrapper
from kafka_wrapper import KafkaWrapper
import data_handler
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
    last_minute = datetime.datetime.now().minute
    consumption = {"consumption_last_24h": -1, "prediction_next_30d": -1}
    
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

            # only send data every minute
            minute = datetime.datetime.now().minute
            if last_minute != minute:
            #if True:
                # Every hour write value to database and do prediction
                hour = datetime.datetime.now().hour
                if last_hour != hour:
                    dh = data_handler.DataHandler()
                    print("writing to database")
                    dh.write_to_db(data)
                    try:
                        consumption = dh.predict()
                    except:
                        print("Prediction failed")
                    last_hour = hour
                
                consumption = {"consumption_last_24h": -1, "prediction_next_30d": -1}
                data.append(consumption)
                print(data)
                
                # Publish data
                mqtt_wrapper.mqtt_publish(data)
                try:
                    kafka_wrapper.kafka_publish(data)
                except:
                    print("Kafka server not running")
                last_minute = minute
        
        # Repeat every second
        time.sleep(1)
