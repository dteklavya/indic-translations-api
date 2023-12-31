from flask import Flask, jsonify, request, json
from translate import BhashiniTranslator
from werkzeug.exceptions import HTTPException


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
    translator.getTranslatorPipeLine()
    return jsonify(translator.translate(text))


@app.errorhandler(HTTPException)
def handle_exception(exception):
    response = exception.get_response()
    response.data = json.dumps(
        {
            "code": exception.code,
            "name": exception.name,
            "description": exception.description,
        }
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(port=5000)
