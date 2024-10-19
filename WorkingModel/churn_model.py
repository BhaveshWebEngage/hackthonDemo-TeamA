# churn_model.py

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def categorize_users_dynamic(df, session_threshold, interaction_days_threshold, purchase_threshold):
    df['churn_category'] = 'Not Churned'  

    df.loc[(df['session_count'] < session_threshold) & 
            (df['last_interaction_days'] > interaction_days_threshold) & 
            (df['total_purchases'] == purchase_threshold), 'churn_category'] = 'Churned'
    
    df.loc[(df['session_count'] < session_threshold) & 
            (df['last_interaction_days'] >= (interaction_days_threshold // 2)) & 
            (df['last_interaction_days'] <= interaction_days_threshold), 'churn_category'] = 'Potentially Churned'
    
    return df

def train_churn_model(filepath, session_threshold=10, interaction_days_threshold=30, purchase_threshold=0):
    # Load the data
    df = pd.read_csv(filepath)

    # Categorize users using dynamic thresholds
    categorized_users_df = categorize_users_dynamic(df, session_threshold, interaction_days_threshold, purchase_threshold)

    # Prepare features and target variable
    X = categorized_users_df[['session_count', 'last_interaction_days', 'total_purchases']]
    y = categorized_users_df['churn_category'].apply(lambda x: 1 if x == 'Churned' else (0 if x == 'Not Churned' else -1)).replace(-1, 0)  # Convert to binary for simplicity

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Evaluate the model
   # print(classification_report(y_test, predictions))

    # Return categorized DataFrame and model
    return categorized_users_df, model
