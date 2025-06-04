import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib

# Load and clean dataset
df = pd.read_csv("dataset/fall_dataset.csv", low_memory=False)

# Drop the first column if it's a timestamp or has mixed types
df = df.iloc[:, 1:]

# Replace labels
df['motion'] = df['motion'].replace({'fall': 1, 'nonfall': 0})

# Split features and labels
X = df.drop('motion', axis=1)
y = df['motion']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train XGBoost Classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(scaler, 'scaler_xgb.pkl')
joblib.dump(model, 'fall_model_xgb.pkl')
