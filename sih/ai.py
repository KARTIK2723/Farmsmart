import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset (after downloading crop_recommendation.csv from Kaggle)
data = pd.read_csv("crop_recommendation.csv")

# Features and labels
X = data.drop("label", axis=1)   # N, P, K, temp, humidity, ph, rainfall
y = data["label"]                # Crop name

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
pickle.dump(model, open("crop_model.pkl", "wb"))
