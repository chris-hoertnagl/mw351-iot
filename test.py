import data_handler
import psycopg2
import pandas as pd

# Connect to an existing database
connection = psycopg2.connect(user="pi",
                              password="pw_raspberry",
                              host="127.0.0.1",
                              port="5432",
                              database="iotdb")
try:
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute("SELECT * from ENERGYMGMT")
    df = pd.DataFrame(cursor.fetchall())
    print("Created df from database")
    df.columns = ["date", "power"]
    df.date = pd.to_datetime(df.date)
    df.power = df.power.astype(float)
    df.to_csv("data.csv")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

dh = data_handler.DataHandler()
print(dh.predict())
