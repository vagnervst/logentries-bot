from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=["POST"])
def welcome():
    print(request.get_json())
    return "The server received your request but thinks you can do better."


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
