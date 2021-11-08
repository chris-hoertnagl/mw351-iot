import psycopg2
from psycopg2 import Error
import pandas as pd
import linreg

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="pi",
                                  password="pw_raspberry",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="iotdb")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute("SELECT * from ENERGYMGMT")
    df = pd.DataFrame(cursor.fetchall())
    print("Create df from database")
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

df.columns = ["date", "power"]
df.date = pd.to_datetime(df.date)
df.power = df.power.astype(float)
print(df)
print(df.info())
print("###################################################")
print(linreg.predict(df))
