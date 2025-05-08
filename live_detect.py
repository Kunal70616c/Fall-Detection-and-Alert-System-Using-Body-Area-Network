import serial
import time
import numpy as np
import joblib
from scipy.stats import skew, kurtosis


# Load scaler and model
scaler = joblib.load('models/scaler.pkl')
model = joblib.load('models/fall_detection_model.pkl')

# Setup serial
ser = serial.Serial('/dev/cu.usbserial-FTB6SPL3', 115200)
time.sleep(2)

# Buffer to store recent samples (6 samples = 6 seconds)
window = []

def extract_features(window):
    window_np = np.array(window)
    accel_mag = np.linalg.norm(window_np[:, 0:3], axis=1)
    gyro_mag = np.linalg.norm(window_np[:, 3:6], axis=1)

    signals = {
        'ax': window_np[:, 0],
        'ay': window_np[:, 1],
        'az': window_np[:, 2],
        'gx': window_np[:, 3],
        'gy': window_np[:, 4],
        'gz': window_np[:, 5],
        'accel_mag': accel_mag,
        'gyro_mag': gyro_mag
    }

    features = []
    for sig in signals.values():
        features.extend([
            np.mean(sig), np.std(sig), np.max(sig), np.min(sig),
            skew(sig), kurtosis(sig)
        ])
    return np.array(features).reshape(1, -1)

while True:
    line = ser.readline().decode().strip()
    if "ax:" in line:
        try:
            parts = line.split(',')
            ax = float(parts[0].split(':')[1].strip().replace('g', ''))
            ay = float(parts[1].split(':')[1].strip().replace('g', ''))
            az = float(parts[2].split(':')[1].strip().replace('g', ''))

            gx = float(parts[3].split(':')[1].strip().replace('deg/s', ''))
            gy = float(parts[4].split(':')[1].strip().replace('deg/s', ''))
            gz = float(parts[5].split(':')[1].strip().replace('deg/s', ''))

            sample = [ax, ay, az, gx, gy, gz]
            window.append(sample)

            if len(window) == 6 :
                features = extract_features(window)
                features_scaled = scaler.transform(features)
                prediction = model.predict(features_scaled)[0]

                label = "FALL DETECTED 🚨" if prediction == 1 else "No Fall"
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Prediction: {label}")
                print(f"AX: {ax}, AY: {ay}, AZ: {az}, GX: {gx}, GY: {gy}, GZ: {gz}")
                # Slide window (50% overlap = remove first 3 samples)
                window = window[1:]

        except Exception as e:
            pass  # ignore errors silently
