# campaign_manager.py

from churn_model import predict_churn
from engagement_system import engage_user
import os
import pandas as pd

def run_campaign(interaction_file):
    print("Running churn detection campaign...")

    # Load interaction data
    data = pd.read_csv(interaction_file)

    at_risk_users = []
    
    for index, row in data.iterrows():
        user_data = row[['session_count', 'average_session_length', 'last_interaction_days', 'total_purchases', 'email_opens', 'push_opens', 'inapp_interactions']].values
        # Predict if the user is likely to churn
        # print(predict_churn(user_data)[0])
        result = predict_churn(user_data)[0]
        print(f'User status {row['user_id']} churn status {result}')
        if result == 1:  # Check if predicted churn is 1
            # print(predict_churn(user_data)[0])
            at_risk_users.append(row['user_id'])

    if not at_risk_users:
        print("No at-risk users detected.")
        return

    # Engage at-risk users
    engage_user(at_risk_users)

    print("Campaign finished.")

if __name__ == "__main__":
    
    # Specify the path to the interactions data file
    interaction_file = os.getcwd()+'/backend/data/test-data.csv'
    
    # Run the campaign
    run_campaign(interaction_file)
