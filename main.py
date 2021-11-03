from mqtt import mqtt_publish
import time
import subprocess

if __name__ == '__main__':

    # Start smlogger via python subprocess as background process
    CMD = ["smlogger", "-a", "169.254.155.71", "-p", "7259"]
    process = subprocess.Popen(CMD, stdout=subprocess.PIPE)

    while True:
        # Read output from smlogger(Writte to txt by pylon smlogger)
        with open("logfile.txt", "r") as f:
            data = f.readlines()
        # Publish data via mqtt and kafka client
        if data != None:
            mqtt_publish(data)
        # Read data from Smart meter every second
        time.sleep(1)
