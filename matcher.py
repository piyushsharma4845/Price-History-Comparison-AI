import pandas as pd
import numpy as np
import datetime
import random
from sklearn.linear_model import LinearRegression

def generate_60_day_history(current_price):
    """Creates a realistic simulated price history for the last 60 days."""
    dates = pd.date_range(end=datetime.datetime.now(), periods=60)
    prices = []
    
    # Start with a price slightly higher than current
    temp_price = current_price * random.uniform(1.05, 1.12)
    
    for i in range(60):
        # Small daily fluctuations
        variation = random.uniform(-0.01, 0.01) * temp_price
        temp_price += variation
        
        # Simulate a price drop (Sale) every 15 days
        if i % 15 == 0:
            temp_price -= (temp_price * random.uniform(0.05, 0.10))
            
        prices.append(round(temp_price, 2))
    
    # Ensure the last day matches the actual current price
    prices[-1] = current_price
    
    return pd.DataFrame({"date": dates, "price": prices})

def predict_future_price(df):
    """Uses Linear Regression (AI) to predict the price for the next 7 days."""
    df['day_index'] = np.arange(len(df))
    X = df[['day_index']]
    y = df['price']
    
    # Train the Machine Learning Model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for 7 days into the future
    future_day = len(df) + 7
    prediction = model.predict([[future_day]])[0]
    
    current_price = y.iloc[-1]
    trend = "UP" if prediction > current_price else "DOWN"
    
    return round(prediction, 2), trend