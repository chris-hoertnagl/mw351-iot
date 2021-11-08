import numpy as np
import pandas as pd
from sklearn import linear_model

data = [("2021-11-08 21:31:53" ,10691.50), ("2021-11-08 21:31:53" ,10691.50), ("2021-11-06 15:00:53",  6000.3), ("2021-11-06 16:00:53",  6000.3), ("2021-11-05 01:31:00",  789.32)]
df = pd.DataFrame(data)
df.columns = ["date", "power"]
df.date = pd.to_datetime(df.date)
df

def predict(df):
    df.sort_values("date", ascending=True, inplace=True)
    df['days_from_start'] = (df.date - df.date.values[0]).dt.days

    X = df['days_from_start'].values[:,np.newaxis] 
    y = df['power'].values

    model = linear_model.LinearRegression()
    model.fit(X, y)

    today = df.days_from_start.max()
    prediction_day = today + 30
    prediciton = model.predict([[prediction_day]])
    print(today)
    print(prediction_day)
    print(prediciton)
    print(df.loc[df.days_from_start == today, "power"][0])

    estimation = prediciton - df.loc[df.days_from_start == today, "power"]
    print(estimation)

    print(f"Estimated Energy consumption for the next 30 days: {estimation}")
    return estimation

predict(df)