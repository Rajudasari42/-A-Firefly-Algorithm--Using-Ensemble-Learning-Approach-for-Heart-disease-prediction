# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
column_names = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
data = pd.read_csv(url, names=column_names)

# Handle missing values and convert to numeric
data = data.replace('?', pd.NA).dropna().astype(float)

# Convert target to binary (0 = No Disease, 1 = Disease)
data['target'] = (data['target'] > 0).astype(int)

# Split data
X = data.drop('target', axis=1)
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing
scaler = StandardScaler()
preprocessor = ColumnTransformer(transformers=[('num', scaler, X.columns)])

# Ensemble model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
voting_clf = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')

# Pipeline
pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', voting_clf)])

# Train model
pipeline.fit(X_train, y_train)

# Evaluate model
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')

# Save model
joblib.dump(pipeline, 'heart_disease_model.pkl')
print("Model saved as 'heart_disease_model.pkl'")
