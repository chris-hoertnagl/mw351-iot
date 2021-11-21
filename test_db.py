import psycopg2
from psycopg2 import Error
import pandas as pd
import numpy as np
from sklearn import linear_model

def predict(df):
    df.sort_values("date", ascending=True, inplace=True)
    df['days_from_start'] = (df.date - df.date.values[0]).dt.days

    X = df['days_from_start'].values[:,np.newaxis] 
    y = df['power'].values

    model = linear_model.LinearRegression()
    model.fit(X, y)

    today = df.days_from_start.max()
    power_cons_today = df.loc[df.days_from_start == today, 'power'].values[0]
    prediction_day = today + 30
    prediciton = model.predict([[prediction_day]])
    
    print(f"consumption today: {power_cons_today}")
    print(f"consumption in 30 days: {prediciton[0]}")

    estimation = prediciton[0] - power_cons_today

    print(f"Estimated Energy consumption for the next 30 days: {estimation}")
    return estimation


if __name__ == '__main__':
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
        print("Created df from database")
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
    df.to_csv("data.csv")
    print(df)
    print(df.info())
    print("###################################################")
    print(predict(df))
