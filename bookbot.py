from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment
API_KEY = os.getenv("API_NINJAS_API_KEY")

# Route to return student number
@app.route('/')
def home():
    return jsonify({"student_number": "200575702"})

# Route to fetch and return quotes based on a category
@app.route('/quotes', methods=['POST'])
def quotes():
    # Extract category from Dialogflow's request JSON
    req = request.get_json(silent=True, force=True)
    category = req.get('queryResult', {}).get('parameters', {}).get('category', 'inspirational')  # Default: 'inspirational'

    # Fetch quote from API Ninjas
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        quote_data = response.json()
        if quote_data:
            quote = quote_data[0].get('quote', "Here's a quote for you!")
            author = quote_data[0].get('author', 'Unknown')
            fulfillment_text = f"'{quote}' - {author}"
        else:
            fulfillment_text = "I couldn't find any quotes in that category. Please try another."
    else:
        fulfillment_text = "Sorry, I couldn't fetch a quote at the moment. Please try again later."

    # Return JSON response for Dialogflow
    return jsonify({"fulfillmentText": fulfillment_text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
