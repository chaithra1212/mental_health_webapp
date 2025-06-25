import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Load dataset
df = pd.read_excel('data/userusage.xlsx')

# Rename columns for consistency
df.rename(columns={
    'screen_time (hrs)': 'screen_time',
    'unlock_count': 'unlock_count',
    'sleep_duration (hrs)': 'sleep_hours',
    'app_usage_social (hrs)': 'app_usage',
    'mood': 'mental_health_status'
}, inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Define features and target
features = ['screen_time', 'unlock_count', 'sleep_hours', 'app_usage']
X = df[features]
y = df['mental_health_status']

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Save the model and label encoder
with open('model/predictor.pkl', 'wb') as f:
    pickle.dump((model, le), f)

print("✅ Model trained and saved to model/predictor.pkl")
