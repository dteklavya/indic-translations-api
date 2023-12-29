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
    translator = BhashiniTranslator()
    translator.getPipeLine(sourceLanguage, targetLanguage)
    return jsonify(translator.pipeLineData)


if __name__ == "__main__":
    app.run(port=5000)
