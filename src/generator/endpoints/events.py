import json
import logging
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from service.engine import Engine

router = APIRouter()

logger = logging.getLogger("generator")


class EventGridData(BaseModel):
    event_time: datetime
    event_data: str


@router.post(
    path="/events",
    responses={
        status.HTTP_200_OK: {"description": "Event grid event received"}
    },
)
async def events(payload: EventGridData):
    """
    Event grid endpoint
    :param payload:
    :return:
    """
    logger.info(f"Event grid event with payload {payload}")
    df_generation_provider = "test2"
    deepfake_engine = Engine()
    try:
        event_data = json.loads(payload.event_data)
        raw_file_name = event_data["blobUrl"].split("/")[-1]
        audio_org_file = deepfake_engine.download_audio_file(blob_name=raw_file_name)

        name, extension = raw_file_name.split(".")
        prefix = deepfake_engine.get_current_file_id()
        df_file_name = f"{prefix}_{name}_FAKE_{df_generation_provider}.{extension}"
        org_file_name = f"{prefix}_{name}_ORGN_{df_generation_provider}.{extension}"

        audio_df_file = deepfake_engine.generate_fake_audio_elevenlabs(audio_org_file)

        deepfake_engine.upload_audio_file(blob_name=df_file_name, audio_df_file=audio_df_file,
                                          blob_directory="deepfakes")
        deepfake_engine.upload_audio_file(blob_name=org_file_name, audio_df_file=audio_org_file,
                                          blob_directory="originals")

        return Response(status_code=status.HTTP_200_OK,
                        content=f"Deepfake for file {org_file_name} was created and uploaded as {df_file_name}.")
    except Exception as e:
        logger.error(f"Error while processing event grid event: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=f"Error while processing event grid event: {e}")
