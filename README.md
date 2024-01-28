# Indic Translations API
Python API to interact with Bhashini (ULCA) APIs - a solution for Indic languages.

## Setup and use

Should work fine with `Python >= 3.10`.

```
pip install -r requirements.txt
```

It uses [Bhashini Translator Package](https://github.com/dteklavya/bhashini_translator) heavily.

Run `Flask` app:

```
flask app --debug
```

At this point, you can use `Postman` or other client for using APIs.

Follwoing end-points are available ATM:

`translate`: Translate text from source to target language.

`tts`: Generate audio for given text.

`asr`: Automatic speech recognition (ASR) for given audio stream(base 64 encoded) and translation to text.

`asr_nmt`: ASR for given audio stream(base 64 encoded) and translation to text in target language.

`nmt_tts`: Translate text to target language and generates audio.

`asr_nmt_tts`: ASR, translation and audio in target languade.


