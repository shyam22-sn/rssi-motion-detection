import subprocess
import csv
import time
from datetime import datetime

INTERFACE = "wlp0s20f3"  # your WiFi interface name
LOG_DURATION = 120       # seconds
OUTPUT_FILE = "../data/rssi_log.csv"

def get_rssi():
    result = subprocess.check_output(["iwconfig", INTERFACE]).decode()
    for line in result.split("\n"):
        if "Signal level" in line:
            parts = line.strip().split("Signal level=")
            if len(parts) > 1:
                rssi = parts[1].split(" ")[0].strip()
                return rssi
    return None

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "RSSI (dBm)"])

    print(f"Logging RSSI for {LOG_DURATION} seconds...")
    start_time = time.time()
    
    while (time.time() - start_time) < LOG_DURATION:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rssi = get_rssi()
        if rssi:
            print(f"{timestamp} | RSSI: {rssi}")
            writer.writerow([timestamp, rssi])
        time.sleep(1)

print("✅ Logging complete. File saved as:", OUTPUT_FILE)

