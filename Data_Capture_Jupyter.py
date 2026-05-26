"""
This is the code to capcture the data from the ESP32 and save it as a .csv file on the laptop.
This is to be run on Jupyter Notebook, so the end of each cell in this code will be demarcated with a comment.
"""

import serial
import pandas as pd
import time
import os

PORT = 'YOUR_COM_PORT'                
DATASET_FILE = 'gesture_dataset.csv'

"""
Cell Break
"""

def collect_samples(label, num_samples=20):
    ser = serial.Serial(PORT, 115200, timeout=2)
    time.sleep(2)  # Wait for serial to stabilize
    ser.reset_input_buffer()
    collected = 0


    print(f"Collecting {num_samples} samples for: '{label}'")
    print("Hold button → draw gesture → release.\n")

    while collected < num_samples:
        input(f"  [{collected+1}/{num_samples}] Draw, then press Enter '{label}'...")
        rows = []

        # Wait until button is pressed (ESP sends IMU data, not IDLE)
        while True:
            line = ser.readline().decode(errors='ignore').strip() # Converts bytes to a string, skipping any errors.
            if ',' in line:
                rows.append(line.split(','))
                break

        # Keep reading until button is released (ESP sends IDLE)
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line == 'IDLE':
                break
            if ',' in line:
                rows.append(line.split(','))

        if len(rows) < 5:
            print("  Too short, skipping.")
            continue

        # Save to CSV
        df = pd.DataFrame(rows, columns=['ax','ay','az','gx','gy','gz'])
        df['label'] = label
        df['sample_id'] = f"{label}_{collected}"
        df.to_csv(DATASET_FILE, mode = 'a', header = not os.path.exists(DATASET_FILE), index = False)

        collected += 1
        print(f"Saved ({len(rows)} rows)")

    ser.close()
    print(f"Done! {num_samples} samples saved for '{label}'.\n")


"""
Cell Break
"""
collect_samples(0)
"""
Cell Break
"""
collect_samples(1)
"""
Here onwards, call the capcture function for every digit that you wish to call.
"""
