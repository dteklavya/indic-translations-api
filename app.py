from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def main():
    return {'msg': "Welcome!"}


if __name__ == "__main__":
    app.run(port=5000)
