import pandas as pd
import random

# Sample data to simulate user interactions
data = {
    'user_id': ['user1', 'user2', 'user3', 'user4'],
    'last_interaction': [pd.Timestamp('2024-10-01'), pd.Timestamp('2024-09-20'), pd.Timestamp('2024-08-15'), pd.Timestamp('2024-07-10')],
    'email': ['user1@example.com', 'user2@example.com', 'user3@example.com', 'user4@example.com'],
    'phone': ['+1234567890', '+1234567891', '+1234567892', '+1234567893'],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define a threshold for inactivity (e.g., 30 days)
threshold_days = 30
threshold_date = pd.Timestamp.now() - pd.Timedelta(days=threshold_days)

# Identify at-risk users
at_risk_users = df[df['last_interaction'] < threshold_date]

# Function to simulate sending notifications
def send_notifications(users):
    for _, user in users.iterrows():
        user_id = user['user_id']
        email = user['email']
        phone = user['phone']
        
        print(f"[PUSH] Sent push notification to user: {user_id}, Message: 'Check out our new features and offers!'")
        
        if user_id == 'user2':  # Specific message for user2 as an example
            print(f"[IN-APP] Sent in-app message to user: {user_id}, Message: 'We've missed you! Here's a 20% discount to re-engage.'")
            print(f"[EMAIL] Sent email to: {email}, Subject: 'Come back!', Message: 'We've missed you! Here's a 20% discount to re-engage.'")
            print(f"[SMS] Sent SMS to: {phone}, Message: 'We've missed you! Here's a 20% discount to re-engage.'")

# Main script to run the churn detection campaign
if not at_risk_users.empty:
    print("Running churn detection campaign...")
    send_notifications(at_risk_users)
    print("Campaign finished.")
else:
    print("No at-risk users detected.")
