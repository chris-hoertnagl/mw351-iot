import numpy as np
import pandas as pd
import datetime
from sklearn import linear_model

def predict(df, hours):
    df['hours_from_start'] = (df.date - df.date[0]).days
    x = df['days_from_start'].values
    y = df['power'].values
    x = x.reshape(-1, 1)

    model = linear_model.LinearRegression().fit(x, y)
    linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

    prediction_day = df.days_from_start.max() + hours
    prediciton = model.predict([[prediction_day]])

    print(f"Energy consumption in {hours} hours will be: {prediciton}")
    return prediciton
