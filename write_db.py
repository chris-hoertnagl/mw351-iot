import psycopg2
from sml_parser import parse
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

def write_to_db(data):
    parsed = parse(data)
    date = pd.to_datetime(parsed[0]['date'])
    power = float(parsed[0]['P'])
    insert_query = f""" INSERT INTO ENERGYMGMT (DATE, POWER) VALUES ({date}, {power})"""

    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()