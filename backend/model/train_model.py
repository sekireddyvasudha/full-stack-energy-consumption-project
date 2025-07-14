import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os


# Load dataset
data = pd.read_csv('../../ENB2012_data.csv')

features = data.iloc[:, 0:8]
target = data.iloc[:, 8]

# Normalize features
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# Save the scaler for future use
import joblib
import os

# Ensure model directory exists
os.makedirs('model', exist_ok=True)

joblib.dump(scaler, 'model/scaler.save')

# Create sequences
def create_sequences(data, target, look_back=5):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i + look_back])
        y.append(target[i + look_back])
    return np.array(X), np.array(y)

X, y = create_sequences(features_scaled, target)

# Build model
model = Sequential()
model.add(Conv1D(64, 2, activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))
model.compile(loss=MeanSquaredError(), optimizer='adam')
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train
early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model.fit(X, y, epochs=100, batch_size=16, verbose=1, callbacks=[early_stop])

# Save model
os.makedirs('model', exist_ok=True)
model.save('model/model.h5')
print("Model trained and saved.")
