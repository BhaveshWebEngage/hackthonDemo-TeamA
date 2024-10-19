import json
import openai
import os

# Constants
API_KEY = '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'  # Replace with your actual API key
BASE_URL = "https://api.groq.com/openai/v1"

# Initialize OpenAI client
client = openai.OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# Generate retention strategy for a user
def generate_retention_strategy(user_data):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert in customer retention strategies."},
            {"role": "user", "content": f"Based on the following user data, suggest a retention strategy: {json.dumps(user_data)}"}
        ]
    )
    m  =[
            {"role": "system", "content": "You are an expert in customer retention strategies."},
            {"role": "user", "content": f"Based on the following user data, suggest a retention strategy: {json.dumps(user_data)}"}
        ]
    print(m)

    if response and response.choices:
        return  response.choices[0].message.content
    else:
        print("Failed to generate retention strategy.")
        return None

# Main function
def main():
    # Load user interaction data
    # user_data_file = '/Volumes/Bhavesh/WebEngage/WorkSpace/Python/RetetionStrategy/backend/user_data.json'  # Ensure your file is in JSON format
    # user_data = load_user_data(user_data_file)

    # Example user data for testing
    new_user_data = {
        "user_id": "user5",
        "session_count": 30,
        "average_session_length": 10,
        "last_interaction_days": 10,
        "total_purchases": 5,
        "email_opens": 0,
        "push_opens": 10,
        "inapp_interactions": 0
    }

    # Generate retention strategy
    strategy = generate_retention_strategy(new_user_data)
    print(f"Recommended Retention Strategy: {strategy}")

if __name__ == "__main__":
    main()