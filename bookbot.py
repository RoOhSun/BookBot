from flask import Flask, jsonify, request # type: ignore

app = Flask(__name__)

# Route 1: Home route to return your student number
@app.route('/')
def home():
    return jsonify({"student_number": "200575702"})

if __name__ == '__main__':
    app.run(debug=True)
