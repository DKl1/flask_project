import json

from flask import Flask, request, Response, session
from waitress import serve
from flask_jwt import JWT, jwt_required, current_identity
from db import Admin

app = Flask(__name__)
app.config["SECRET_KEY"] = "a61e4c9b93f3f0682250b6cf833"
jwt = JWT(app, Admin.auth)

@app.route('/')
def index():
    return "first page"


@app.route('/api/v1/hello-world-07')
def about():
    return "Hello World 7"


@app.route('/login', methods=['POST'])
def loginAdmin():
    admin_json = request.get_json()
    if Admin.auth(admin_json['username'], admin_json['password']):
        session['logged_in'] = True
    return Response(f"Status: {200}", status=200)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


if __name__ == '__main__':
    app.run(debug=True, port=3000)
    print("Server")
    serve(app)

# curl -X POST -H "Content-Type: application/json" \
#  -d '{"username": "admin3000", "password": "pass"}' \
#  "http://localhost:3000/login"