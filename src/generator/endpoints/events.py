import logging

from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from service.engine import Engine

router = APIRouter()

logger = logging.getLogger("generator")


class EventGridData(BaseModel):
    ...


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
    deepfake_engine = Engine()
    audio_org_file = deepfake_engine.download_audio_file()
    audio_df_file = deepfake_engine.generate_fake_audio_elevenlabs(audio_org_file)
    deepfake_engine.upload_audio_file(audio_df_file)
    return Response(status_code=status.HTTP_200_OK)
