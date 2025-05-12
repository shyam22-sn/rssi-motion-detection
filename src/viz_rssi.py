import pandas as pd
import matplotlib.pyplot as plt

# Read and clean data
df = pd.read_csv("../data/rssi_log.csv")

# Rename columns if extra whitespace exists
df.columns = [col.strip() for col in df.columns]

# Drop rows with missing values
df.dropna(inplace=True)

# Convert types
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
df["RSSI (dBm)"] = pd.to_numeric(df["RSSI (dBm)"], errors='coerce')

# Drop rows that failed conversion
df.dropna(inplace=True)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df["Timestamp"].values, df["RSSI (dBm)"].values, marker='o', linestyle='-')
plt.title("WiFi RSSI over Time")
plt.xlabel("Time")
plt.ylabel("Signal Strength (dBm)")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.gca().invert_yaxis()  # Stronger signal = higher
plt.show()

