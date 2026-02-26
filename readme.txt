# 🌫️ Air Pollution AI – AQI Forecasting Using LSTM

## 📌 Project Overview

Air pollution in Delhi NCR shows severe seasonal variation, especially during winters.  
This project uses **Deep Learning (LSTM)** to predict future AQI (Air Quality Index) values based on historical data.

The model analyzes past AQI trends and forecasts the next day’s AQI using time-series forecasting techniques.

---

## 🧠 Algorithm Used

This project uses:

**LSTM (Long Short-Term Memory Network)**  
- Type: Recurrent Neural Network (RNN)  
- Suitable for: Time Series Forecasting  
- Handles sequential and temporal data  

A 30-day sliding window approach is used to predict the next day's AQI.

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn (MinMaxScaler)
- TensorFlow / Keras
- Streamlit (for dashboard)

---

## 📂 Project Structure
air_pollution_ai/
│
├── app/
│ └── dashboard.py
│
├── data/
│ └── delhi_aqi.csv
│
├── model/
│ └── aqi_lstm.h5
│
├── train.py
├── requirements.txt
└── README.md


---

## ⚙️ Model Architecture

- LSTM Layer (64 units, return_sequences=True)
- LSTM Layer (32 units)
- Dense Layer (1 output neuron)
- Optimizer: Adam
- Loss Function: Mean Squared Error (MSE)
- Epochs: 20
- Batch Size: 32

---

## 📊 How It Works

1. Load historical AQI dataset
2. Convert date column to datetime format
3. Normalize AQI values using MinMaxScaler
4. Create 30-day time window sequences
5. Train LSTM model
6. Predict next day AQI
7. Save trained model

---
