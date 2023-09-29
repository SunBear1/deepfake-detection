import os
import shutil

from starlette import status
from starlette.responses import Response
from fastapi import FastAPI, HTTPException, UploadFile, File, Form

import elevenLabsLogic
from engine import Engine

API_KEY = os.getenv("API_KEY")
if API_KEY == "":
    raise Exception("ElevenLabs API_KEY not set")

testAPI = elevenLabsLogic.ElevenLabsAPI(apiKey=API_KEY)

app = FastAPI()

engine = Engine()


@app.post("/create_voice")
async def create_voice(file: UploadFile = File(...)):
    try:
        directory = os.getcwd() + os.sep + file.filename.split(".")[0]
        os.makedirs(directory, exist_ok=True)
        new_filename = os.path.join(directory, file.filename)
        file_bytes = file.file.read()
        with open(new_filename, "wb") as f:
            f.write(file_bytes)

        id = engine.get_current_file_id(directory_name="originals")
        engine.upload_audio_file(
            blob_name=f"{id}_{file.filename}_ORGN.mp3",
            audio_df_file=file_bytes,
            blob_directory="deepfakes",
        )

        testAPI.createOwnVoice(
            name=file.filename,
            pathToVoicesDir=directory,
            description=f"{file.filename}",
        )
        shutil.rmtree(directory)

        return Response(
            status_code=status.HTTP_201_CREATED,
            content=f"Voice {file.filename} created successfully",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_voices")
async def list_voices():
    try:
        voices = testAPI.listVoices()
        return Response(status_code=status.HTTP_200_OK, content={"voices": voices})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_voice/{voiceID}")
async def delete_voice(voiceID: str):
    try:
        testAPI.deleteVoice(voiceID)
        return Response(
            status_code=status.HTTP_200_OK,
            content={"message": "Voice deleted successfully"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/use_voice/{voiceID}")
async def use_voice(voiceID: str, text: str = Form(...)):
    try:
        audio = testAPI.readTexts(
            text=text,
            voice=voiceID,
        )
        id = engine.get_current_file_id(directory_name="deepfakes")
        voiceName = testAPI.getNameByVoiceID(voiceID)
        engine.upload_audio_file(
            blob_name=f"{id}_{voiceName}_FAKE_11labs.mp3",
            audio_df_file=audio,
            blob_directory="deepfakes",
        )
        return Response(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Text {id}_{voiceName}_FAKE_11labs.mp3 generated and saved successfully"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
