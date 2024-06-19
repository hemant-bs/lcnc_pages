from flask import Flask
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

user = 'jane'
pw = '1234'
users = {
    user: pw
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username), password
    return False


@app.route('/hello')
@auth.login_required
def hello_world():
    return 'Hello, World!'



if __name__ == '__main__':
    print('Starting app')
    app.run(debug=True, port=8070)