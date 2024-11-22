from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

#Route for student number
@app.route('/')
def home():
    return jsonify({
        "student_name": "Roshan Khatri" , 
        "student_number": "200575702"
        
    })



# Route for Dialogflow fulfillment
@app.route('/fulfillment', methods=['POST'])
def fulfillment():
    req = request.get_json()
    # Extract the ingredient parameter from Dialogflow
    ingredient = req['queryResult']['parameters'].get('ingredient', '')

    if not ingredient:
        return jsonify({
            "fulfillmentText": "I couldn't find the ingredient in your request."
        })

    # Call the Themealdb API
    try:
        api_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
        response = requests.get(api_url)
        data = response.json()

        if data['meals']:
            # Extract recipe names
            recipes = [meal['strMeal'] for meal in data['meals']]
            recipe_list = ', '.join(recipes)
            reply = f"Here are some recipes with {ingredient}: {recipe_list}."
        else:
            reply = f"Sorry, I couldn't find recipes with {ingredient}."

        return jsonify({
            "fulfillmentText": reply
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "fulfillmentText": "Sorry, something went wrong while fetching recipes."
        })

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
