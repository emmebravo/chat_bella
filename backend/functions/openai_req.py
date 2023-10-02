import openai
from decouple import config

from functions.database import get_recent_messages

# env var
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# OpenAI (whisper)
def speech_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as error:
        print(error)
        return


# OpenAI (chatGPT)
def get_chat_res(message_input):
    messages = get_recent_messages
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        print(res)
        message_as_text = res["choices"][0]["message"]["content"]
        return message_as_text
    except Exception as error:
        print(error)
        return
