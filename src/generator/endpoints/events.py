import logging

from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

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
    return Response(status_code=status.HTTP_200_OK)
