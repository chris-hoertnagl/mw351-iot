from kafka import KafkaConsumer

consumer = KafkaConsumer(
        'EnergyMgmt',
         bootstrap_servers="IWILR3-7.CAMPUS.fh-ludwigshafen.de:9092",
         auto_offset_reset='earliest',
         #enable_auto_commit=True,
         #group_id='my-group',
         #value_deserializer=lambda x: loads(x.decode('utf-8'))
          )

for message in consumer:
    print(message.value)