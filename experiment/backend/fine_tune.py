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

def prepare_data(user_interactions):
    """Prepare data in prompt-completion format for fine-tuning."""
    training_data = []
    for interaction in user_interactions:
        prompt = (
            f"Based on the following user data: {json.dumps(interaction['user_data'])}, "
            f"what retention strategy would you suggest?"
        )
        completion = interaction['retention_strategy']
        training_data.append({"prompt": prompt, "completion": completion})
    return training_data

def save_training_data(training_data, file_path):
    """Save the training data to a JSONL file."""
    with open(file_path, 'w') as f:
        for entry in training_data:
            f.write(json.dumps(entry) + "\n")

def upload_dataset(file_path):
    """Upload the dataset to OpenAI and return the dataset ID."""
    with open(file_path, 'rb') as f:
        response = client.files.create(file=f, purpose='fine-tune')
    return response['id']

def fine_tune_model(dataset_id):
    """Fine-tune the model using the uploaded dataset."""
    response = client.fine_tuning.jobs.create(
        training_file=dataset_id,
        model="bhavesh-191024",  # Replace with the base model ID you want to fine-tune
        n_epochs=4,                   # Adjust as necessary
        batch_size=16                 # Adjust as necessary
    )
    return response

def main():
    # Example user interactions data
    user_interactions = [
        {
            "user_data": {
                "user_id": "user1",
                "session_count": 15,
                "average_session_length": 5,
                "last_interaction_days": 2,
                "total_purchases": 3,
                "email_opens": 10,
                "push_opens": 5,
                "inapp_interactions": 1
            },
            "retention_strategy": "Send personalized emails and offer discounts."
        },
        {
            "user_data": {
                "user_id": "user2",
                "session_count": 5,
                "average_session_length": 3,
                "last_interaction_days": 10,
                "total_purchases": 1,
                "email_opens": 2,
                "push_opens": 0,
                "inapp_interactions": 0
            },
            "retention_strategy": "Re-engagement campaign through push notifications."
        },
        # Add more user interaction data as needed
    ]

    # Prepare the training data
    training_data = prepare_data(user_interactions)

    # Save the training data to a JSONL file
    training_file_path = 'fine_tunning_dataset.json'
    save_training_data(training_data, training_file_path)

    # Upload the dataset
    dataset_id = upload_dataset(training_file_path)
    print(f"Uploaded dataset ID: {dataset_id}")

    # Fine-tune the model
    fine_tune_response = fine_tune_model(dataset_id)
    print(f"Fine-tuning response: {fine_tune_response}")

if __name__ == "__main__":
    main()
