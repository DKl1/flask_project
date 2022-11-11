from flask import Flask
from waitress import serve
app = Flask(__name__)


@app.route('/')
def index():
    return "first page"


@app.route('/api/v1/hello-world-07')
def about():
    return "Hello World 7"


if __name__ == '__main__':
    app.run(debug=True, port=3000)
    print("Server")
    serve(app)
