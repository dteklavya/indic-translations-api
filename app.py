from flask import Flask, jsonify, request
from translate import BhashiniTranslator


app = Flask(__name__)


@app.route("/")
def home():
    return {"msg": "Welcome!"}


@app.route("/translate", methods=["POST"])
def translate():
    sourceLanguage = request.json.get("sourceLanguage")
    targetLanguage = request.json.get("targetLanguage")
    text = request.json.get("text")
    translator = BhashiniTranslator(sourceLanguage, targetLanguage)
    translator.getPipeLine()
    return jsonify(translator.translate(text))


if __name__ == "__main__":
    app.run(port=5000)
