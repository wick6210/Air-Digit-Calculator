"""
This program is to extract the meaningful features from the collected dataset.
Since this was run on Jupyter Notebook, the cell breaks are mentioned as comments in the program.
"""

import numpy as np
import pandas as pd

DATASET_FILE  = 'gesture_dataset.csv'
FEATURES_FILE = 'features.csv'

"""
Cell Break
"""

def extract_features(rows):
    # rows: (N, 6) — all IMU readings for one gesture
    # returns: 36 numbers summarising the gesture
    features = []
    for col in range(6):                          # for each axis
        s = rows[:, col]
        features += [np.mean(s), np.std(s),
                     np.min(s),  np.max(s),
                     np.max(s) - np.min(s),        # range
                     np.sqrt(np.mean(s**2))]       # RMS
    return features

df = pd.read_csv(DATASET_FILE)
print(f"Raw data: {len(df)} rows, {df['sample_id'].nunique()} gestures")

X, y = [], []

for sid, group in df.groupby('sample_id'):
    rows = group[['ax','ay','az','gx','gy','gz']].values.astype(float)
    X.append(extract_features(rows))
    y.append(group['label'].iloc[0])

features_df = pd.DataFrame(X)
features_df.insert(0, 'label', y)

features_df.to_csv(FEATURES_FILE, index=False)
print(f"Saved {len(features_df)} feature vectors → '{FEATURES_FILE}'")
features_df.head()

df = pd.read_csv('features.csv')
print(df['label'].value_counts())
print(f"\nTotal samples: {len(df)}")
