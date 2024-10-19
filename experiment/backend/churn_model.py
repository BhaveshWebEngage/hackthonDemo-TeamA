import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

# Load interaction data
filepath = os.getcwd() + '/backend/data/interactions_data.csv'
data = pd.read_csv(filepath)

# Features based on user interaction
features = ['session_count', 'average_session_length', 'last_interaction_days', 'total_purchases', 'email_opens', 'push_opens', 'inapp_interactions']
X = data[features]

# Modify churn column to represent 3 classes: 0 (churned), 1 (potentially churned), 2 (not churned)
# Here we assume that data['churned'] currently holds binary values (1 for churned, 0 for active)
# We need to transform these values into three categories based on custom logic
# Example logic (this can be adjusted based on your own thresholds):
# - 0: churned (already churned)
# - 1: potentially churned (high last_interaction_days or low session_count, etc.)
# - 2: not churned (active users)

def categorize_churn(row):
    if row['churned'] == 1:
        return 0  # Churned
    if row['last_interaction_days'] > 30 or row['session_count'] < 5:  # Example threshold
        return 1  # Potentially churned
    else:
        return 2  # Not churned

data['churn_category'] = data.apply(categorize_churn, axis=1)

y = data['churn_category']  # Updated target variable with 3 classes

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model - Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Performance
print(classification_report(y_test, y_pred))

def predict_churn(user_data):
    """Predict if a user is likely to churn based on their interactions."""
    prediction = model.predict([user_data])
    return prediction  # Return the predicted category (0, 1, or 2)

# Example usage
# user_data = [session_count, average_session_length, last_interaction_days, total_purchases, email_opens, push_opens, inapp_interactions]
# prediction = predict_churn(user_data)
# print("Predicted category:", prediction)
