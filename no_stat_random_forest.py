import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Load dataset
df = pd.read_csv("dataset/fall_dataset.csv")  # Replace with your dataset path

# Automatically drop non-numeric or non-useful columns
if 'time' in df.columns:
    df.drop(columns=['time'], inplace=True)


# Automatically fix label column
if 'motion' in df.columns:
    df['motion'] = df['motion'].str.strip().str.lower()
    df['motion'] = df['motion'].replace({'fall': 1, 'nonfall': 0})
else:
    raise ValueError("Expected a column named 'motion' for labels.")

# Check for missing values
if df.isnull().sum().sum() > 0:
    df = df.dropna()

# Separate features and labels
X = df.drop('motion', axis=1)
y = df['motion']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model and scaler
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fall_detection_model_v2.pkl")
joblib.dump(scaler, "models/scaler_v2.pkl")

print("\n✅ Model and scaler saved in 'models/' directory.")
