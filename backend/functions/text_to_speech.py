import requests

from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


# text to speech
def convert_text_to_speech(message):
    # message body
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        },
    }

    # voice
    voice_bella = "EXAVITQu4vr4xnSDxMaL"

    # headers
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    }

    # endpoint
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_bella}"

    # send req
    try:
        res = requests.post(endpoint, json=body, headers=headers)
    except Exception as error:
        return error

    # handle res
    if res.status_code == 200:
        return res.content
    else:
        return
