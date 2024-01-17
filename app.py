from flask import Flask, jsonify, request, json, send_file
from dotenv import load_dotenv

from bhashini_translator import Bhashini
from werkzeug.exceptions import HTTPException
import io
import base64


app = Flask(__name__)
load_dotenv()


@app.route("/")
def home():
    return {"msg": "Welcome!"}


@app.route("/translate", methods=["POST"])
def translate():
    sourceLanguage = request.json.get("sourceLanguage")
    targetLanguage = request.json.get("targetLanguage")
    text = request.json.get("text")
    translator = Bhashini(sourceLanguage, targetLanguage)
    return jsonify(translator.translate(text))


@app.route("/tts", methods=["POST"])
def tts():
    sourceLanguage = request.json.get("sourceLanguage")
    text = request.json.get("text")
    translator = Bhashini(sourceLanguage)

    base64String = translator.tts(text)
    decodedData = base64.b64decode(base64String)
    wav_file = "/tmp/tts.wav"
    with open(wav_file, "wb") as wavFh:
        wavFh.write(decodedData)

    return send_file(wav_file, mimetype="audio/wav")


@app.route("/asr_nmt", methods=["POST"])
def ars_nmt():
    sourceLanguage = request.json.get("sourceLanguage")
    targetLanguage = request.json.get("targetLanguage")
    base64String = request.json.get("base64String")

    translator = Bhashini(sourceLanguage, targetLanguage)
    text = translator.asr_nmt(base64String)
    return jsonify(text)


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
