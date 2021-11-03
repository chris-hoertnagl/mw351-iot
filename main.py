from mqtt import MqttWrapper
import time
import subprocess

if __name__ == '__main__':

    # Start smlogger via python subprocess as background process
    CMD = ["smlogger", "-a", "169.254.155.71", "-p", "7259"]
    process = subprocess.Popen(CMD, stdout=subprocess.PIPE)

    mqtt_wrapper = MqttWrapper()

    while True:
        # Read output from smlogger (written to logfile.txt by pylon smlogger)
        with open("logfile.txt", "r") as f:
            data = f.readlines()
        # Publish data via mqtt and kafka client
        if  not data:
            mqtt_wrapper.mqtt_publish(data)
        # Repeat every second
        time.sleep(1)
