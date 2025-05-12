import pandas as pd
import numpy as np

# Load the RSSI CSV
df = pd.read_csv("../data/rssi_log.csv")
df.columns = [col.strip() for col in df.columns]  # clean headers

# Convert RSSI to numeric
df["RSSI (dBm)"] = pd.to_numeric(df["RSSI (dBm)"], errors='coerce')
df.dropna(inplace=True)

# Sliding window parameters
window_size = 5  # 5 seconds
step_size = 1    # slide by 1 second

features = []

for start in range(0, len(df) - window_size + 1, step_size):
    window = df["RSSI (dBm)"].iloc[start:start + window_size].values
    mean = np.mean(window)
    var = np.var(window)
    std = np.std(window)
    timestamp = df["Timestamp"].iloc[start + window_size - 1]  # last time in window

    features.append([timestamp, mean, var, std])

# Save to CSV
features_df = pd.DataFrame(features, columns=["Timestamp", "Mean", "Variance", "StdDev"])
features_df.to_csv("../data/rssi_features.csv", index=False)

print("✅ Features extracted and saved to rssi_features.csv")

