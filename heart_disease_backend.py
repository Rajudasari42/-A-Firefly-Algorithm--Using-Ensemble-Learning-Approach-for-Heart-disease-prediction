from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Moved here after initializing app

# Load the trained model
try:
    model = joblib.load('heart_disease_model.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Home Route
@app.route('/')
def home():
    return "Heart Disease Prediction API is running. Use /predict to make predictions."

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = pd.DataFrame([data['features']], columns=[
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ])
        prediction = model.predict(features)[0]
        print("Model Prediction:", prediction)
        result = "High Risk" if prediction == 1 else "Low Risk"
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




