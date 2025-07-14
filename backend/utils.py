import os
from tensorflow.keras.models import load_model
import joblib
def predict_energy_consumption(input_data):
    input_array = np.array(input_data, dtype=np.float32).reshape(1, 5, 8)
    input_scaled = scaler.transform(input_array.reshape(-1, 8)).reshape(1, 5, 8)
    prediction = model.predict(input_scaled)
    return prediction[0][0]

def predict_energy_consumption(input_data):
    # process input_data (likely a NumPy array or list)
    prediction = model.predict(input_data)
    return prediction.tolist()  # or just return prediction

base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, 'model', 'model.h5')
scaler_path = os.path.join(base_path, 'model', 'scaler.save')

model = load_model(model_path, compile=False)

scaler = joblib.load(scaler_path)
