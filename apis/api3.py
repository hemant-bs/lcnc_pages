from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Dummy data
data = {
    "users": [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Alice"},
        {"id": 3, "name": "Bob"},
    ]
}

# Dummy token for demonstration purposes
dummy_token = 'mhfihih9949403039491293'

# Token verification function
@auth.verify_token
def verify_token(token):
    return token == dummy_token

# POST endpoint to add data (requires Bearer Token authentication)
@app.route('/api/add_data', methods=['POST'])
@auth.login_required
def add_data():
    new_data = request.get_json()
    data.append(new_data)
    return jsonify({"message": "Data added successfully"})

# GET endpoint to retrieve all data
@app.route('/api/get_data', methods=['GET'])
@auth.login_required
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
