import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

file = "data/delhi_aqi.csv"
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[["aqi"]])

X = []
y = []

window = 30
for i in range(window, len(scaled)):
    X.append(scaled[i-window:i, 0])
    y.append(scaled[i, 0])

X, y = np.array(X), np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], 1)),
    LSTM(32),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")
model.fit(X, y, epochs=20, batch_size=32)

model.save("model/aqi_lstm.h5")
print("Model trained and saved!")