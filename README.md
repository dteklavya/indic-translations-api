# Indic Translations API
Python API to interact with Bhashini (ULCA) APIs - a solution for Indic languages.

## Setup and use

Should work fine with `Python >= 3.10`.

```
pip install -r requirements.txt
```

It uses [Bhashini Translator Package](https://github.com/dteklavya/bhashini_translator) heavily. Make sure to [read the instructions](https://github.com/dteklavya/bhashini_translator?tab=readme-ov-file#pythonic-bhashini-translator) to setup your environment with API keys and others.

Aslo add `SECRET_KEY` and `DEBUG` to your environment for Django.

Create a user to test the API: ```python transBharat/manage.py createsuperuser```

Run `Django` app:

```
python transBharat/manage.py runserver
```

At this point, you can use `Postman` or other client for using APIs. Or visit [Swagger end-point](http://localhost:8000/api/schema/swagger-ui/) to play with.

Follwoing end-points are available ATM:

`translate`: Translate text from source to target language.

`tts`: Generate audio for given text.

`asr`: Automatic speech recognition (ASR) for given audio stream(base 64 encoded) and translation to text.

`asr_nmt`: ASR for given audio stream(base 64 encoded) and translation to text in target language.

`nmt_tts`: Translate text to target language and generates audio.

`asr_nmt_tts`: ASR, translation and audio in target language.


