import paho.mqtt.client as paho
from parser import parse
import datetime

def publish(data):
    broker="IWILR3-6.CAMPUS.fh-ludwigshafen.de" 
    port=1883
    if data != None:
                   topics, payloads = parse(data) 
                   bret_client = paho.Client("Bret")
                   bret_client.connect(broker, port)
                   for x in range(4):
    	                bret_client.publish(topics[x], payloads[x], qos=0, retain=False)


