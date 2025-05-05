import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from scipy.stats import skew, kurtosis
import warnings

warnings.filterwarnings("ignore")

# --- Load and preprocess the data ---
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path, low_memory=False)

    # Drop 'time' column
    if 'time' in data.columns:
        data = data.drop(columns=['time'])

    # Rename columns
    data = data.rename(columns={
        'ax': 'accel_x',
        'ay': 'accel_y',
        'az': 'accel_z',
        'w': 'gyro_w',
        'x': 'gyro_x',
        'y': 'gyro_y',
        'z': 'gyro_z',
        'droll': 'gyro_droll',
        'dpitch': 'gyro_dpitch',
        'dyaw': 'gyro_dyaw',
        'motion': 'fall_label'
    })

    # Clean up label case and map to 0/1
    data['fall_label'] = data['fall_label'].astype(str).str.lower().map({'nonfall': 0, 'fall': 1})

    # Drop rows with NaNs
    data = data.dropna()

    return data

# --- Feature extraction per window ---
def calculate_window_features(window):
    features = {}

    accel_mag = np.sqrt(window['accel_x']**2 + window['accel_y']**2 + window['accel_z']**2)
    gyro_mag = np.sqrt(window['gyro_droll']**2 + window['gyro_dpitch']**2 + window['gyro_dyaw']**2)

    signals = {
        'accel_x': window['accel_x'],
        'accel_y': window['accel_y'],
        'accel_z': window['accel_z'],
        'gyro_droll': window['gyro_droll'],
        'gyro_dpitch': window['gyro_dpitch'],
        'gyro_dyaw': window['gyro_dyaw'],
        'accel_mag': accel_mag,
        'gyro_mag': gyro_mag
    }

    for name, signal in signals.items():
        features[f'{name}_mean'] = signal.mean()
        features[f'{name}_std'] = signal.std()
        features[f'{name}_max'] = signal.max()
        features[f'{name}_min'] = signal.min()
        features[f'{name}_skew'] = skew(signal)
        features[f'{name}_kurt'] = kurtosis(signal)

    return features

# --- Create dataset from windows ---
def create_feature_label_dataset(data, window_size=6, overlap=0.5):
    step = int(window_size * (1 - overlap))
    X, y = [], []

    for start in range(0, len(data) - window_size + 1, step):
        end = start + window_size
        window = data.iloc[start:end]

        if window.shape[0] == window_size:
            label = window['fall_label'].mode()[0]
            features = calculate_window_features(window)
            X.append(features)
            y.append(label)

    return pd.DataFrame(X), pd.Series(y)

# --- Main pipeline ---
if __name__ == '__main__':
    file_path = 'dataset.csv'
    data = load_and_preprocess_data(file_path)

    print(f"[INFO] Raw samples after cleaning: {len(data)}")

    X, y = create_feature_label_dataset(data, window_size=6, overlap=0.5)

    print(f"[INFO] Extracted {X.shape[0]} samples with {X.shape[1]} features.")

    if X.empty:
        raise ValueError("No samples extracted from dataset. Check your input file and preprocessing steps.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred):.2f}")
    print(f"Recall: {recall_score(y_test, y_pred):.2f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


    joblib.dump(clf, 'fall_detection_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("✅ Model and scaler saved as 'fall_detection_model.pkl' and 'scaler.pkl'.")
