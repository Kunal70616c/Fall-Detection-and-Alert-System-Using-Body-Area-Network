import requests
import numpy as np
import joblib
from scipy.stats import skew, kurtosis
from location_scripts.send_alert_email import send_fall_alert_email

# Load model and scaler
scaler = joblib.load('models/scaler.pkl')
model = joblib.load('models/fall_detection_model.pkl')

# ThingSpeak channel and keys
READ_API_KEY = 'OU6JHCBWGXY9JXJO'
CHANNEL_ID_SENSOR = '2979884'
CHANNEL_ID_GPS = '2979886'

# User and location details
USER_NAME = "Test Subject 1"
DEFAULT_LATITUDE = 22.5906
DEFAULT_LONGITUDE = 88.2644

def fetch_latest_samples(n=6):
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID_SENSOR}/feeds.json"
    params = {'api_key': READ_API_KEY, 'results': n}
    r = requests.get(url, params=params)
    feeds = r.json().get("feeds", [])
    window = []
    for feed in feeds:
        try:
            ax = float(feed["field1"])
            ay = float(feed["field2"])
            az = float(feed["field3"])
            gx = float(feed["field4"])
            gy = float(feed["field5"])
            gz = float(feed["field6"])
            window.append([ax, ay, az, gx, gy, gz])
        except:
            continue
    return window if len(window) == n else None

def fetch_latest_gps():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID_GPS}/feeds/last.json"
    params = {'api_key': 'F2T9DYK8KJL8BBF5'}
    try:
        r = requests.get(url, params=params)
        data = r.json()
        lat = float(data["field1"])
        lon = float(data["field2"])
        return lat, lon
    except:
        return DEFAULT_LATITUDE, DEFAULT_LONGITUDE

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

def predict_fall_and_alert():
    window = fetch_latest_samples()
    if not window:
        print("❌ Insufficient sensor data from ThingSpeak.")
        return {"status": "error", "message": "Insufficient sensor data."}

    features = extract_features(window)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]

    if prediction == 1:
        print("🚨 FALL DETECTED!")
        lat, lon = fetch_latest_gps()
        send_fall_alert_email(True, lat, lon, USER_NAME)
        return {
            "status": "success",
            "fall_detected": True,
            "location": {"latitude": lat, "longitude": lon}
        }
    else:
        print("✅ No Fall Detected.")
        return {
            "status": "success",
            "fall_detected": False
        }
