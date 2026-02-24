import pandas as pd

IN_FILE = "data/processed_aqi_data.csv"
OUT_FILE = "data/delhi_aqi.csv"

# Load Kaggle CSV
df = pd.read_csv(IN_FILE)

# ---- 1) Detect datetime column (common Kaggle names) ----
datetime_candidates = ["Datetime", "datetime", "date_time", "timestamp", "time", "DateTime", "date"]
dt_col = next((c for c in datetime_candidates if c in df.columns), None)
if dt_col is None:
    raise ValueError(f"❌ Datetime column not found. Columns: {list(df.columns)}")

df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")
df = df.dropna(subset=[dt_col])

# ---- 2) Detect AQI column ----
aqi_candidates = ["AQI", "aqi", "overall_aqi", "AQI_Value", "Air Quality Index"]
aqi_col = next((c for c in aqi_candidates if c in df.columns), None)
if aqi_col is None:
    raise ValueError(f"❌ AQI column not found. Columns: {list(df.columns)}")

# ---- 3) Filter only Delhi if city column exists ----
city_candidates = ["City", "city", "location", "Location"]
city_col = next((c for c in city_candidates if c in df.columns), None)

if city_col is not None:
    # Keep rows that contain 'delhi' (case-insensitive)
    df = df[df[city_col].astype(str).str.lower().str.contains("delhi", na=False)]

# ---- 4) Convert to daily average AQI ----
df["date"] = df[dt_col].dt.date
daily = df.groupby("date", as_index=False)[aqi_col].mean()
daily.rename(columns={aqi_col: "aqi"}, inplace=True)

daily.to_csv(OUT_FILE, index=False)

print("✅ Converted Kaggle hourly data to daily AQI!")
print("✅ Saved:", OUT_FILE)
print(daily.head(10))
print("Rows:", len(daily))