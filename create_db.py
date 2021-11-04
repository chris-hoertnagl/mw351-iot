import psycopg2
from parser import parse

class SQLWrapper:
    def __init__(self):
        topic_1 = "EnergyMgmt/SM000001/Power"
        topic_2 = "EnergyMgmt/SM000001/Current"
        topic_3 = "EnergyMgmt/SM000001/Voltage"
        topic_4 = "EnergyMgmt/SM000001/CounterReading"
        self.topics = [topic_1, topic_2, topic_3, topic_4]
    def insert(self, data):
        #establishing the connection
        conn = psycopg2.connect(database="mydb", user='postgres', password='iot', host='127.0.0.1', port= '5432')
        conn.autocommit = True
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        #Preparing query to create a database
        #sql = '''CREATE database mydb'''
        #Creating a database
        #sql ="Select * From EnergyMgmt2"
        payloads = parse(data)
        #print(payloads[x].split(",")[0].split(":",maxsplit=1)[1]) #zeit
        #print(self.topics[0])
        for x in range(len(self.topics)):
            try:
                v1 = payloads[x].split(",")[1].split(":",maxsplit=1)[1].replace("}","")
            except:
                v1 = ""
            try:
                v2 = payloads[x].split(",")[2].split(":",maxsplit=1)[1].replace("}","")
            except:
                v2 = ""
            try:
                v3 = payloads[x].split(",")[3].split(":",maxsplit=1)[1].replace("}","")
            except:
                v3 = ""
            try:
                v4 = payloads[x].split(",")[4].split(":",maxsplit=1)[1].replace("}","")
            except:
                v4 = ""
            date =  str(payloads[x].split(",")[0].split(":",maxsplit=1)[1])
            #try:
            sql ="Insert into EnergyMgmt2 (Date_SM ,Topic, v1 , v2, v3, v4) values ('" + date  + \
                                                                                          "','" + self.topics[x] +"','" + str(v1) + "','" + str(v2) + "','" + str(v3) +"','" + str(v4) + "')"
            cursor.execute(sql)
            #except:
               # pass
        #print(cursor.fetchone())
        #cursor2 = cursor.fetchall()
        #for x in cursor:
        #print(x)
        #print("Database created successfully........")
        #print("Tabelle erfolgreich erstellt")
        #Closing the connection
        conn.close()

