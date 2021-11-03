from kafka import KafkaConsumer

consumer = KafkaConsumer('EnergyMgmt')
for message in consumer:
    print (message)