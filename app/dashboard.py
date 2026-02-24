import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1) Load Data (Fix File Path)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # air_pollution_ai/
CSV_PATH = os.path.join(BASE_DIR, "data", "delhi_aqi.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

# -----------------------------
# 2) Basic Cleaning
# -----------------------------
# Try to parse a date column if present
date_col_candidates = ["date", "Date", "datetime", "Datetime", "timestamp", "Timestamp"]
date_col = None
for c in date_col_candidates:
    if c in df.columns:
        date_col = c
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values(by=date_col)

# Find AQI column
aqi_col_candidates = ["aqi", "AQI", "Aqi", "pm2_5_aqi", "PM2.5_AQI"]
aqi_col = None
for c in aqi_col_candidates:
    if c in df.columns:
        aqi_col = c
        break

if aqi_col is None:
    # fallback: try to guess numeric column that looks like AQI
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(numeric_cols) > 0:
        aqi_col = numeric_cols[0]
    else:
        raise ValueError("No numeric columns found to use as AQI. Please check your CSV columns.")

# Remove missing AQI rows
df = df.dropna(subset=[aqi_col]).copy()

# -----------------------------
# 3) AQI Category Helper
# -----------------------------
def aqi_category(aqi_value: float) -> str:
    # Common AQI buckets (India/US style)
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Satisfactory"
    elif aqi_value <= 200:
        return "Moderate"
    elif aqi_value <= 300:
        return "Poor"
    elif aqi_value <= 400:
        return "Very Poor"
    else:
        return "Severe"

# Add category column
df["AQI_Category"] = df[aqi_col].apply(aqi_category)

# -----------------------------
# 4) Streamlit Dashboard
# -----------------------------
import streamlit as st

st.set_page_config(page_title="Delhi AQI Dashboard", layout="wide")

st.title("🌫️ Delhi Air Quality Dashboard")
st.caption(f"Data source file: {CSV_PATH}")

# Sidebar filters
st.sidebar.header("Filters")

# Date filter (if date available)
if date_col:
    min_date = df[date_col].min()
    max_date = df[date_col].max()

    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

    # Apply date range
    mask = (df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)
    dff = df.loc[mask].copy()
else:
    dff = df.copy()
    st.sidebar.info("No date column detected in CSV, date filter disabled.")

# Category filter
categories = ["All"] + sorted(dff["AQI_Category"].unique().tolist())
selected_cat = st.sidebar.selectbox("AQI Category", categories)

if selected_cat != "All":
    dff = dff[dff["AQI_Category"] == selected_cat]

# -----------------------------
# 5) KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

latest_aqi = float(dff[aqi_col].iloc[-1]) if len(dff) > 0 else np.nan
avg_aqi = float(dff[aqi_col].mean()) if len(dff) > 0 else np.nan
max_aqi = float(dff[aqi_col].max()) if len(dff) > 0 else np.nan
min_aqi = float(dff[aqi_col].min()) if len(dff) > 0 else np.nan

with col1:
    st.metric("Latest AQI", f"{latest_aqi:.0f}" if np.isfinite(latest_aqi) else "NA")
with col2:
    st.metric("Average AQI", f"{avg_aqi:.0f}" if np.isfinite(avg_aqi) else "NA")
with col3:
    st.metric("Max AQI", f"{max_aqi:.0f}" if np.isfinite(max_aqi) else "NA")
with col4:
    st.metric("Min AQI", f"{min_aqi:.0f}" if np.isfinite(min_aqi) else "NA")

# -----------------------------
# 6) Charts
# -----------------------------
left, right = st.columns((2, 1))

with left:
    st.subheader("📈 AQI Trend")
    if date_col:
        plot_df = dff.dropna(subset=[date_col, aqi_col])
        fig, ax = plt.subplots()
        ax.plot(plot_df[date_col], plot_df[aqi_col])
        ax.set_xlabel("Date")
        ax.set_ylabel("AQI")
        ax.set_title("AQI Over Time")
        st.pyplot(fig)
    else:
        st.warning("No date column found, cannot plot trend over time.")

with right:
    st.subheader("📊 AQI Category Distribution")
    cat_counts = dff["AQI_Category"].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.bar(cat_counts.index, cat_counts.values)
    ax2.set_xlabel("Category")
    ax2.set_ylabel("Count")
    ax2.set_title("Category Counts")
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)

# -----------------------------
# 7) Data Preview
# -----------------------------
st.subheader("🧾 Data Preview")
st.dataframe(dff.tail(50), use_container_width=True)

# -----------------------------
# 8) Download Filtered CSV
# -----------------------------
st.subheader("⬇️ Download Filtered Data")
csv_bytes = dff.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_bytes,
    file_name="filtered_delhi_aqi.csv",
    mime="text/csv"
)