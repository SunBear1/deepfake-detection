import os
import shutil

from starlette import status
from starlette.responses import Response, JSONResponse
from fastapi import APIRouter, UploadFile, File, Form

from service.eleven_labs_client import ElevenLabsClient
from service.engine import Engine

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise Exception("ElevenLabs API_KEY not set")

eleven_labs_client = ElevenLabsClient(apiKey=API_KEY)

router = APIRouter()

engine = Engine()


@router.post("/voices")
async def create_voice(file: UploadFile = File(...)):
    file_path = os.getcwd() + os.sep + file.filename.split(".")[0]
    os.makedirs(file_path, exist_ok=True)
    new_filename = os.path.join(file_path, file.filename)
    file_bytes = file.file.read()
    with open(new_filename, "wb") as f:
        f.write(file_bytes)

    file_id = engine.get_current_file_id(directory_name="originals")

    eleven_labs_client.create_voice(
        name=file.filename,
        path_to_voices_dir=file_path,
        description=file.filename,
    )

    engine.upload_audio_file(
        blob_name=f"{file_id}_{file.filename}_ORGN.mp3",
        audio_df_file=file_bytes,
        blob_directory="originals",
    )

    shutil.rmtree(file_path)

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=f"Voice {file.filename} created successfully",
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
async def use_voice(voice_id: str, text: str = Form(...)):
    audio = eleven_labs_client.read_text(
        text=text,
        voice=voice_id,
    )
    file_id = engine.get_current_file_id(directory_name="deepfakes")
    voice_name = eleven_labs_client.get_voice_name_by_id(voice_id)
    engine.upload_audio_file(
        blob_name=f"{file_id}_{voice_name}_FAKE_11labs.mp3",
        audio_df_file=audio,
        blob_directory="deepfakes",
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Text spoken by voice {file_id}_{voice_name}_FAKE_11labs.mp3 generated and saved successfully",
    )
