"""
This Jupyter Notebook code is to train the various models and select the best model out of the given options.
The cell breaks have been mentioned as comments in the code
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

FEATURES_FILE = 'features.csv'
CLASSES = ['0','1','2'] # List the number of classes (digits) that you will be considering for your implementation

"""
Cell Break
"""

# Load data
df = pd.read_csv(FEATURES_FILE)
X  = df.drop(columns=['label']).values
y  = df['label'].values
print(f"Loaded: {X.shape[0]} samples, {X.shape[1]} features")

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (KNN is distance-based, so scaling matters)
scaler     = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

"""
Cell Break
"""

# Train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_sc, y_train)
y_pred = knn.predict(X_test_sc)

acc = knn.score(X_test_sc, y_test)
print(f"Accuracy: {acc*100:.1f}%")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred, labels=CLASSES)

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap='Blues')

ax.set_xticks(range(len(CLASSES))); ax.set_xticklabels(CLASSES)
ax.set_yticks(range(len(CLASSES))); ax.set_yticklabels(CLASSES)

plt.colorbar(im, ax=ax)

for i in range(len(CLASSES)):
    for j in range(len(CLASSES)):
        ax.text(j, i, cm[i,j], ha='center', va='center', color='black')

plt.title('Confusion Matrix — KNN')
plt.ylabel('True'); plt.xlabel('Predicted')
plt.tight_layout(); plt.show()

"""
Cell Break
"""

# Random Forest
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_sc, y_train)
y_pred = rf.predict(X_test_sc)

acc_rf = rf.score(X_test_sc, y_test)
print(f"Random Forest Accuracy: {acc_rf*100:.1f}%")
print(classification_report(y_test, y_pred))


cm = confusion_matrix(y_test, y_pred, labels=CLASSES)

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap='Blues')

ax.set_xticks(range(len(CLASSES))); ax.set_xticklabels(CLASSES)
ax.set_yticks(range(len(CLASSES))); ax.set_yticklabels(CLASSES)

plt.colorbar(im, ax=ax)

for i in range(len(CLASSES)):
    for j in range(len(CLASSES)):
        ax.text(j, i, cm[i,j], ha='center', va='center', color='black')

plt.title('Confusion Matrix — RF')
plt.ylabel('True'); plt.xlabel('Predicted')
plt.tight_layout(); plt.show()

"""
Cell Break
"""

# Summary comparison
print(f"KNN           → {acc*100:.1f}%")
print(f"Random Forest → {acc_rf*100:.1f}%")
