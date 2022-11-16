import json
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, Response, session, jsonify, make_response
from waitress import serve
from flask_jwt import JWT, jwt_required, current_identity
from db import Admin
import jwt
app = Flask(__name__)
app.config["SECRET_KEY"] = "a61e4c9b93f3f0682250b6cf833"
# jwt = JWT(app, Admin.auth)

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)

    return decorated

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

        token = jwt.encode({
            'user': admin_json['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route('/protected')
# @jwt_required()
@token_required
def protected():
    return make_response('Success', 200)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
    print("Server")
    serve(app)

# curl -X POST -H "Content-Type: application/json" \
#  -d '{"username": "admin3000", "password": "pass"}' \
#  "http://localhost:3000/login"