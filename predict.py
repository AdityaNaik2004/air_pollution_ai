import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

df = pd.read_csv("data/delhi_aqi.csv")
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[["aqi"]])

window = 30
last_30 = scaled[-window:]

model = load_model("model/aqi_lstm.h5")

future = []
input_seq = last_30

for _ in range(7):
    pred = model.predict(np.reshape(input_seq, (1, window, 1)))
    future.append(pred[0][0])
    input_seq = np.vstack([input_seq[1:], pred])

future_aqi = scaler.inverse_transform(np.array(future).reshape(-1, 1))

print("NEXT 7 DAYS AQI:", future_aqi.flatten())