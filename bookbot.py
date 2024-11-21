from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment
API_KEY = os.getenv("API_NINJAS_API_KEY")

# Route to return student number (for testing)
@app.route('/')
def home():
    return jsonify({"student_number": "200575702"})

# Route to fetch and return quotes based on a category
@app.route('/quotes', methods=['POST'])
def quotes():
    # Extract the request data from Dialogflow's request JSON
    req = request.get_json(silent=True, force=True)
    
    # Check if the 'category' parameter exists in the request from Dialogflow
    category = req.get('queryResult', {}).get('parameters', {}).get('category', 'inspirational')  # Default to 'inspirational'

    # Fetch quote from API Ninjas based on the category
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        quote_data = response.json()
        
        # If a quote is found, extract it
        if quote_data:
            quote = quote_data[0].get('quote', "Here's a quote for you!")
            author = quote_data[0].get('author', 'Unknown')
            fulfillment_text = f"'{quote}' - {author}"
        else:
            # If no quote is found in the category, return a default message
            fulfillment_text = "I couldn't find any quotes in that category. Please try another."
    else:
        # If there's an issue with the API request, return an error message
        fulfillment_text = "Sorry, I couldn't fetch a quote at the moment. Please try again later."

    # Return the response formatted for Dialogflow
    return jsonify({
        "fulfillmentText": fulfillment_text,
        # Optionally, you can return other fields like fulfillment messages or data
        # "fulfillmentMessages": [{"text": {"text": [fulfillment_text]}}]
    })

if __name__ == '__main__':
    # Ensure the app runs on the correct port (use environment variable or default to 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
