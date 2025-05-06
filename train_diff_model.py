import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
#from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import skew, kurtosis
import joblib
import warnings
warnings.filterwarnings("ignore")

# --- Load and preprocess the data ---
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)

    if 'time' in df.columns:
        df = df.drop(columns=['time'])

    df = df.rename(columns={
        'ax': 'accel_x', 'ay': 'accel_y', 'az': 'accel_z',
        'w': 'gyro_w', 'x': 'gyro_x', 'y': 'gyro_y', 'z': 'gyro_z',
        'droll': 'gyro_droll', 'dpitch': 'gyro_dpitch', 'dyaw': 'gyro_dyaw',
        'motion': 'fall_label'
    })

    df['fall_label'] = df['fall_label'].astype(str).str.lower().map({'nonfall': 0, 'fall': 1})
    df = df.dropna()
    return df

# --- Feature extraction ---
def calculate_window_features(window):
    features = {}
    accel_mag = np.sqrt(window['accel_x']**2 + window['accel_y']**2 + window['accel_z']**2)
    gyro_mag = np.sqrt(window['gyro_droll']**2 + window['gyro_dpitch']**2 + window['gyro_dyaw']**2)

    signals = {
        'accel_x': window['accel_x'], 'accel_y': window['accel_y'], 'accel_z': window['accel_z'],
        'gyro_droll': window['gyro_droll'], 'gyro_dpitch': window['gyro_dpitch'], 'gyro_dyaw': window['gyro_dyaw'],
        'accel_mag': accel_mag, 'gyro_mag': gyro_mag
    }

    for name, signal in signals.items():
        features[f'{name}_mean'] = signal.mean()
        features[f'{name}_std'] = signal.std()
        features[f'{name}_max'] = signal.max()
        features[f'{name}_min'] = signal.min()
        features[f'{name}_skew'] = skew(signal)
        features[f'{name}_kurt'] = kurtosis(signal)

    return features

# --- Windowing the dataset ---
def create_feature_label_dataset(data, window_size=6, overlap=0.5):
    step = int(window_size * (1 - overlap))
    X, y = [], []

    for start in range(0, len(data) - window_size + 1, step):
        end = start + window_size
        window = data.iloc[start:end]
        if window.shape[0] == window_size:
            features = calculate_window_features(window)
            label = window['fall_label'].mode()[0]
            X.append(features)
            y.append(label)

    return pd.DataFrame(X), pd.Series(y)

# --- Evaluation ---
def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        'model': model,
        'name': name,
        'accuracy': accuracy_score(y_test, preds),
        'precision': precision_score(y_test, preds),
        'recall': recall_score(y_test, preds),
        'f1': f1_score(y_test, preds)
    }

# --- Main ---
if __name__ == "__main__":
    data = load_and_preprocess_data("dataset/fall_dataset.csv")
    print(f"[INFO] Cleaned dataset: {len(data)} samples")

    X, y = create_feature_label_dataset(data, window_size=6, overlap=0.5)
    print(f"[INFO] Extracted {X.shape[0]} windows with {X.shape[1]} features")

    # Impute NaNs safely
    X = X.fillna(X.median())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y, random_state=42
    )

    models = [
        ("RandomForest", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("XGBoost", XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
        ("GradientBoost", GradientBoostingClassifier(random_state=42)),
    ]

    results = []
    for name, model in models:
        print(f"Training {name}...")
        result = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        results.append(result)

    # Print comparison
    print("\n=== Model Comparison ===")
    print(f"{'Model':<15} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
    for r in results:
        print(f"{r['name']:<15} {r['accuracy']:.4f}     {r['precision']:.4f}     {r['recall']:.4f}     {r['f1']:.4f}")

    # Save best model
    best_model = max(results, key=lambda x: x['f1'])
    joblib.dump(best_model['model'], 'models/best_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    print(f"\n✅ Saved best model: {best_model['name']} with F1-score = {best_model['f1']:.4f}")
