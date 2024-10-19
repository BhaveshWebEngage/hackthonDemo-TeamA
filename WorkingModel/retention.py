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


new_user_data1 = {
    "user_id": "user5",
    "churned_status":'At Risk',
    "session_count": 30,
    "average_session_length": 10,
    "last_interaction_days": 10,
    "total_purchases": 5,
    "email_clicked": 0,
    "push_clicked": 10,
    "inapp_clicked": 0,
    "churned_status": "At Risk",
    "retention_strategy_channels": {
        "Push": {
            "why": "as user is iteracting more with push notification",
            "campaign_content": "How was your purchased product !! click here to avail discounts on new products"
        },
        "In-App": {
             "why": "user is not interacting with campaigns",
            "deprioritize": "true",
            "how": "send them push campaign about opt out from InApp if not usable"
        },
        "Email": {
            "why": "user is not interacting with campaigns",
            "deprioritize": "true",
            "how": "send them push campaign about opt out from email if not usable"
        }
    }
}


# Desired JSON structure format
format_structure = {
    "user": "user5",
    "churned_status": "At Risk",
    "retention_strategy_channels": {
        "Push": {
            "why": "[Reason for using push notifications]",
            "campaign_content": "[Content to send in the push campaign]"
        },
        "In-App": {
            "why": "[Reason for focusing on in-app engagement]",
            "campaign_content": "[Content to send in the in-app campaign]"
        },
        "Email": {
            "why": "[Reason for deprioritizing email]",
            "deprioritize": "true or false",
            "how": "[How to still engage the user through email]"
        }
    }
}

# Generate retention strategy for a user
def generate_retention_strategy(user_data):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert in customer retention strategies. Think from the point of view of channels (email, push, in-app, inline, WhatsApp, Viber). training set of data is {json.dumps(user_data)}"
                },
                {
                    "role": "user",
                    "content": (
                        f"Based on the following user data, suggest a retention strategy: {json.dumps(user_data)}. "
                        "Provide only the output in valid JSON format with no additional commentary. "
                        "The JSON structure should include user_id, churned_status, and retention_strategy_channels. "
                        "Inside retention_strategy_channels, use the channel name as key and provide a map with the following keys: why, campaign_content, deprioritize, and how. "
                        "Ensure that the JSON is well-formed and includes all necessary closing braces."
                    )
                }
            ]
        )



        # Print the raw response for debugging
        if response and response.choices:
            raw_response = response.choices[0].message.content
            # Attempt to parse the response as JSON
            try:
                json_response = json.loads(raw_response)
                print("Parsed JSON Response:", json_response)  # Successfully parsed JSON
                return json_response
            except json.JSONDecodeError:
                print("The response is not valid JSON.")
                print("Response Content:", raw_response)  # Log the problematic response content
                return None
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
        "churned_status":'At Risk',
        "session_count": 30,
        "average_session_length": 10,
        "last_interaction_days": 10,
        "total_purchases": 5,
        "email_clicked": 0,
        "push_clicked": 10,
        "inapp_clicked": 0
    }

    # Generate retention strategy
    strategy = generate_retention_strategy(new_user_data)
    print(f"Recommended Retention Strategy: {strategy}")

if __name__ == "__main__":
    main()