# uvicorn main:app
# uvicorn main:app --reload
# source venv/bin/activate

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse  # send audio file back
from fastapi.middleware.cors import CORSMiddleware
from decouple import config  # import env
import openai

# fcn imports
from functions.openai_req import speech_to_text, get_chat_res
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()

# CORS
origins = ["http://localhost:5173", "http://localhost:4173"]
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# CORS - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

# OpenAPI env var
openai.organization = config("OPEN_AI_ORG")
openai.API_KEY = config("OPEN_AI_KEY")


@app.get("/health")
async def check_health():
    return {"message": "healthy"}


@app.get("/reset")
async def reset_convo():
    reset_messages()
    return {"message": "data reset"}


# post bot response
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # safe temp audio
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # decode speech
    message_decoded = speech_to_text(audio_input)

    # guard to ensure decode
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")

    # get chat res
    chat_res = get_chat_res(message_decoded)

    if not chat_res:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # store messages
    store_messages(message_decoded, chat_res)

    # convert res to audio
    audio_output = convert_text_to_speech(chat_res)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get EleveLabs response")

    # create generator
    def interfile():
        yield audio_output

    # return audio message
    return StreamingResponse(interfile(), media_type="application/octet-stream")
