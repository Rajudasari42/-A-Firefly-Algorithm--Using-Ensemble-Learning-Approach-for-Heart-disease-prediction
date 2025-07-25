import pandas as pd
import joblib

# Load the model
model_path = r'C:\Users\srinu\OneDrive\Desktop\miniproject\heart_disease_model.pkl'
try:
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Test data (example input — adjust if needed)
test_data = pd.DataFrame([[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]],
                         columns=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
                                  "exang", "oldpeak", "slope", "ca", "thal"])

# Make prediction
try:
    prediction = model.predict(test_data)[0]
    result = "High Risk" if prediction == 1 else "Low Risk"
    print(f'Test Prediction: {result}')
except Exception as e:
    print(f"Error during prediction: {e}")
