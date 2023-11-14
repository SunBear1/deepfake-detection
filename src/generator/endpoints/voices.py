import os
import shutil
import requests

from starlette import status
from starlette.responses import Response, JSONResponse
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel


from service.eleven_labs_client import ElevenLabsClient
from service.engine import Engine

API_KEY = "cda54a7eb8c234e10da1b7efe61c24c9"
if not API_KEY:
    raise Exception("ElevenLabs API_KEY not set")

eleven_labs_client = ElevenLabsClient(apiKey=API_KEY)

router = APIRouter()

engine = Engine()


class UseVoicePayload(BaseModel):
    text: str
    subdir: str


@router.post("/voices")
async def create_voice(file: UploadFile = File(...)):
    file_path = os.getcwd() + os.sep + file.filename.split(".")[0]
    os.makedirs(file_path, exist_ok=True)
    new_filename = os.path.join(file_path, file.filename)
    file_bytes = file.file.read()
    with open(new_filename, "wb") as f:
        f.write(file_bytes)

    file_id = engine.get_current_file_id(directory_name="originals")

    response = requests.post(
        url="https://api.elevenlabs.io/v1/voices/add",
        files={"file": open(file_path, "rb")},
        data={"name": file.filename},
        headers={"xi-api-key": API_KEY}
    )

    if response.status_code != 200:
        raise Exception(f"Error occurred during creating a clone of a voice from file {file.filename}. "
                        f"Error: {response}")
    voice_id = response.content.decode("utf-8").split(" ")[-1]
    print(f"Voice {file.filename} created successfully with ID {voice_id}")

    voice_id = eleven_labs_client.get_voice_id_by_name(
        voice_name=file.filename)

    engine.upload_audio_file(
        blob_name=f"{file_id}_{file.filename}_ORGN.mp3",
        audio_df_file=file_bytes,
        blob_directory="originals",
    )

    shutil.rmtree(file_path)

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=f"Voice {file.filename} created successfully with ID {voice_id}",
    )


@router.get("/voices")
async def voices():
    voices_in_use = eleven_labs_client.list_voices()
    return JSONResponse(status_code=status.HTTP_200_OK, content=voices_in_use)


@router.delete("/voice/{voice_id}")
async def delete_voice(voice_id: str):
    eleven_labs_client.delete_voice(voice_id=voice_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        content=f"Voice with id {voice_id} deleted successfully"
    )


@router.put("/voice/{voice_id}")
async def use_voice(voice_id: str, payload: UseVoicePayload):

    URL = f"https://api.elevenlabs.io/v1/{voice_id}?output_format=pcm_24000"
    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
    }
    data = {
        "text": payload.text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0,
            "use_speaker_boost": True
        }
    }

    request = requests.post(URL, headers=headers, json=data)

    # audio = eleven_labs_client.read_text(
    #     text=payload.text,
    #     voice=voice_id,
    # )

    file_id = engine.get_current_file_id(directory_name="deepfakes")
    voice_name = eleven_labs_client.get_voice_name_by_id(voice_id)
    filenameID = payload.subdir.replace(os.sep, '-')
    engine.upload_audio_file(
        blob_name=f"{filenameID}_FAKE_11labs.flac",
        audio_df_file=request.content,
        blob_directory=f"deepfakesFLAC{os.sep}{payload.subdir[:-4]}",
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Text spoken by voice {file_id}_{voice_name}_FAKE_11labs.mp3 generated and saved successfully",
    )
