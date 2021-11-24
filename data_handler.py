import json
import datetime
import psycopg2
import pandas as pd
import numpy as np
from sklearn import linear_model


class DataHandler:
    def __init__(self):
        self.table_name = "ENERGYMGMT"

        # Connect to an existing database
        self.connection = psycopg2.connect(user="pi",
                                      password="pw_raspberry",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="iotdb")

    def write_to_db(self, data):
        parsed = data
        date = pd.to_datetime(parsed[0]['date'])
        power = float(parsed[3]['CR_P'])
        insert_query = """ INSERT INTO ENERGYMGMT (DATE, POWER) VALUES (%s, %s)"""
        item_tuple = (date, power)
        cursor = self.connection.cursor()
        cursor.execute(insert_query, item_tuple)
        self.connection.commit()
    
    def read_from_db(self):
        try:
            # Create a cursor to perform database operations
            cursor = self.connection.cursor()
            cursor.execute("SELECT * from ENERGYMGMT")
            df = pd.DataFrame(cursor.fetchall())
            print("Created df from database")
            df.columns = ["date", "power"]
            df.date = pd.to_datetime(df.date)
            df.power = df.power.astype(float)
            return df
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return None

    def predict(self):
        with open("linreg_settings.json", "r") as f:
                settings = json.load(f)
        regression_days = settings["regression_days"]
        prediciton_days = settings["prediction_days"]
        df = self.read_from_db()
        if df is not None:
            df.sort_values("date", ascending=True, inplace=True)
            now = datetime.datetime.now() - datetime.timedelta(days = regression_days)
            df = df.loc[df.date >= now, :]
            df['hours_from_start'] = round((df.date - df.date.values[0]).dt.total_seconds() / 3600)
            X = df['hours_from_start'].values[:,np.newaxis] 
            y = df['power'].values
            model = linear_model.LinearRegression()
            model.fit(X, y)
            current_hour = df.hours_from_start.max()
            power_cons_now = df.loc[df.hours_from_start == current_hour, 'power'].values[0]
            power_cons_last_24h = (df.tail(1)['power'].values - df.head(1)['power'].values)[0] / regression_days
            prediction_hour = current_hour + (24 * prediciton_days)
            prediciton_raw = model.predict([[prediction_hour]])
            prediction = prediciton_raw[0] - power_cons_now
            print(f"consumption now: {power_cons_now}")
            print(f"consumption over last 24 hours: {power_cons_last_24h}")
            print(f"consumption over the next {prediciton_days} days: {prediction}")
            result = {"consumption_last_24h": power_cons_last_24h, "prediction": prediction, "prediction_settings": settings}
        else:
            result = {"consumption_last_24h": -1, "prediction": -1, "prediction_settings": settings}
        return result