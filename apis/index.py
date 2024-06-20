from flask import Flask, Response , jsonify, request, abort
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from flask_httpauth import HTTPBasicAuth
from io import BytesIO

app = Flask(__name__)


auth = HTTPBasicAuth()
# Dummy data
data = {
    "users": [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Alice"},
        {"id": 3, "name": "Bob"},
    ]
}

users = {
    "admin": "123"
}

# allowed_ips = ['180.148.46.139']  # Add the IP addresses you want to allow

# @app.before_request
# def restrict_ips():
#     client_ip = request.remote_addr
#     if client_ip not in allowed_ips:
#         abort(403) 

# Verify the provided credentials
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# GET endpoint to retrieve user data

@app.route('/api/users', methods=['GET'])
def get_users():
    name_param = request.args.get('name')
    if name_param:
        for user in data["users"]:
            if user["name"] == name_param:
                user = user
                break
        if user:
            return jsonify(user)
    return jsonify(data["users"])

# POST endpoint to add a new user
@app.route('/api/users', methods=['POST'])
@auth.login_required
def add_user():
    new_user = {}
    new_user["name"]  = request.form.get('name')
    new_user["id"] = len(data["users"]) + 1
    data["users"].append(new_user)
    return jsonify(new_user), 201


@app.route('/api/users?name=', methods=['GET'])
@auth.login_required
def get_user_by_name():
    name_param = request.args.get('name')
    for user in data["users"]:
        if user["name"] == name_param:
            user = user
            break
    if user:
        return jsonify(user)
    else:
        return "User not found", 404
    

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()

    # Create a PDF document using ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create a table with sample data
    data = [
        ["Name", "Age"],
        ["Alice", "30"],
        ["Bob", "25"],
        ["Charlie", "35"]
    ]
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    # Set the response headers for PDF content
    buffer.seek(0)
    return Response(buffer.read(), mimetype='application/pdf')

@app.route('/api/add_new_user', methods=['POST'])
@auth.login_required
def add_new_user():
    # Access raw form data using request.data
    raw_data = request.data
    if raw_data:
        try:
            # Decode and process the raw data (assuming it's in a specific format)
            new_user_name = raw_data.decode('utf-8')
            new_user = {"id": len(data["users"]) + 1, "name": new_user_name}
            data["users"].append(new_user)
            return jsonify(new_user), 201
        except UnicodeDecodeError:
            return "Invalid data format", 400
    else:
        return "Bad Request: Data missing", 400

# PUT endpoint to update a user's information
@app.route('/api/users/<string:user_name>', methods=['PUT'])
@auth.login_required
def update_user(user_name):
    user = next((user for user in data["users"] if user["name"] == user_name), None)
    if user:
        updated_user_data = extract_name(request.data)
        if updated_user_data:
            user["name"] = updated_user_data
            return jsonify(user), 200
        else:
            return "Bad Request: 'new_name' parameter missing", 400
    else:
        return "User not found", 404

# PATCH endpoint to partially update a user's information
@app.route('/api/users/<string:user_name>', methods=['PATCH'])
@auth.login_required
def patch_user(user_name):
    user = next((user for user in data["users"] if user["name"] == user_name), None)
    
    if user:
        updated_user_data = request.form.get('new_name')
        if updated_user_data:
            user["name"] = updated_user_data
            return jsonify(user), 200
        else:
            return "Bad Request: 'new_name' parameter missing", 400
    else:
        return "User not found", 404

# DELETE endpoint to remove a user
@app.route('/api/users/<string:user_name>', methods=['DELETE'])
@auth.login_required
def delete_user(user_name):
    user = next((user for user in data["users"] if user["name"] == user_name), None)
    if user:
        data["users"].remove(user)
        return "User deleted", 204
    else:
        return "User not found", 404


@app.route('/api/resource', methods=['GET'])
@auth.login_required
def get_resource():
    accept_header = request.headers.get('temp')
    if accept_header:
        # Check the value of the Accept header
        if '123' in accept_header:
            response_data = {"message": "Resource in JSON format"}
            return jsonify(response_data)
        else:
            return "Unsupported Media Type", 415  # Return a 415 Unsupported Media Type response
    else:
        # If no Accept header is provided, you can choose a default format
        return "Unsupported Media Type", 415

def extract_name(raw_data):
    if raw_data:
        try:
            new_user_name = raw_data.decode('utf-8')
            return new_user_name
        except UnicodeDecodeError:
            return None
        
@app.route('/headers')
def print_headers():
    headers = request.headers
    headers = dict(request.headers)
    print("Request Headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")
    return jsonify(headers)


if __name__ == '__main__':
    app.run(debug=True)