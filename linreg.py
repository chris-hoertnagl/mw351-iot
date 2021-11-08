import numpy as np
import pandas as pd
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