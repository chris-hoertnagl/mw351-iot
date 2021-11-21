import psycopg2
import pandas as pd

database = "iotdb"
user = 'pi',
password = 'pw_raspberry'
host = '127.0.0.1'
port = '5432'

table_name = "ENERGYMGMT"

# Connect to an existing database
connection = psycopg2.connect(user="pi",
                              password="pw_raspberry",
                              host="127.0.0.1",
                              port="5432",
                              database="iotdb")

df = pd.read_csv("data.csv", parse_dates=["date"], index_col=0)
pl = []
p = 0
for i in range(len(df)):
    pl.append(p)
    p += (30 / (1000))
df['new'] = pl

for i in range(len(df)):
    date = df['date'][i]
    power = df['new'][i]
    update_query = """UPDATE ENERGYMGMT SET power = (%s) WHERE date = (%s)"""
    update_tuple = (power,date)
    cursor = connection.cursor()
    cursor.execute(update_query, update_tuple)
    connection.commit()
