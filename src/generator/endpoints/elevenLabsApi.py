import json
import logging
from datetime import datetime

from fastapi import APIRouter, FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import elevenLabsLogic
import os

API_KEY = "a8412809ee48754b006d19396dd7eb40"

# API_KEY = os.getenv("API_KEY")
# if API_KEY == "":
#     raise Exception("ElevenLabs API_KEY not set")

testAPI = elevenLabsLogic.ElevenLabsAPI(apiKey=API_KEY)

app = FastAPI()

logger = logging.getLogger("generator")


class CreateVoicePayload(BaseModel):
    name: str
    audio_file: UploadFile
    description: str

class SetVoicePayload(BaseModel):
    selected_voice: str

class ReadTextsPayload(BaseModel):
    path_to_texts_file: str
    path_to_save_files_dir: str
    base_filename: str



@app.post("/create_voice/")
async def create_voice(payload: CreateVoicePayload):
    try:
        logger.info("Event grid event with payload {payload.audio_file.filename}")
        uploaded_file_path = "{os.getcwd()}{os.sep}{payload.audio_file.filename}"
        file_bytes = await payload.audio_file.read()
        with open(uploaded_file_path, "wb") as f:
            f.write(file_bytes)

        testAPI.createOwnVoice(
            name=payload.name,
            pathToVoicesDir=uploaded_file_path,
            description=payload.description
        )

        os.remove(uploaded_file_path)

        return {"message": "Voice {payload.name} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set_voice/")
async def set_voice(payload: SetVoicePayload):
    try:
        testAPI.setVoice(payload.selected_voice)
        return {"message": "Voice set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete_voice/")
async def delete_voice():
    try:
        testAPI.deleteVoice()
        return {"message": "Voice deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_voices/")
async def list_voices():
    try:
        voices = testAPI.listVoices()  
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_voice_set/")
async def list_voices():
    try:
        voice = testAPI.getVoice()  
        return {"voice_set": voice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/read_texts/")
async def read_texts(payload: ReadTextsPayload):
    try:
        testAPI.readTexts(
            pathToTextsFile=payload.path_to_texts_file,
            pathToSavefilesDir=payload.path_to_save_files_dir,
            baseFilename=payload.base_filename
        )
        return {"message": "Texts read successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

