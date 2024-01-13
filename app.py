from flask import Flask, jsonify, request, json, send_file
from dotenv import load_dotenv

from bhashini_translator import Bhashini
from werkzeug.exceptions import HTTPException
import io


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
    tts = Bhashini(sourceLanguage)
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
