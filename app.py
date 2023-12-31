from flask import Flask, jsonify, request, json, send_file
from translate import BhashiniTranslator
from werkzeug.exceptions import HTTPException
import io


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


@app.route("/tts", methods=["POST"])
def tts():
    sourceLanguage = request.json.get("sourceLanguage")
    text = request.json.get("text")
    tts = BhashiniTranslator(sourceLanguage)
    tts.getTTSPipeLine()
    audio_file = tts.tts(text)
    with open(audio_file, "rb") as af:
        outBytes = io.BytesIO(af.read())

    return send_file(outBytes, mimetype="audio/wav")


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
