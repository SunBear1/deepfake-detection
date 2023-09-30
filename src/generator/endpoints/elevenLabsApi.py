import os
import shutil

from starlette import status
from starlette.responses import Response
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

import generator.service.elevenLabsLogic as elevenLabsLogic
from service.engine import Engine

API_KEY = os.getenv("API_KEY")
if API_KEY == "":
    raise Exception("ElevenLabs API_KEY not set")

testAPI = elevenLabsLogic.ElevenLabsAPI(apiKey=API_KEY)

router = APIRouter()

engine = Engine()


@router.post("/voices")
async def create_voice(file: UploadFile = File(...)):
    try:
        file_path = os.getcwd() + os.sep + file.filename.split(".")[0]
        os.makedirs(file_path, exist_ok=True)
        new_filename = os.path.join(file_path, file.filename)
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
            pathToVoicesDir=file_path,
            description=file.filename,
        )
        shutil.rmtree(file_path)

        return Response(
            status_code=status.HTTP_201_CREATED,
            content=f"Voice {file.filename} created successfully",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/voices")
async def voices():
    try:
        voices = testAPI.listVoices()
        return Response(status_code=status.HTTP_200_OK, content={"voices": voices})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/voice/{voiceID}")
async def delete_voice(voiceID: str):
    try:
        testAPI.deleteVoice(voiceID)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Voice deleted successfully"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/voice/{voiceID}")
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
