import logging

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter()

logger = logging.getLogger("generator")


@router.get(
    "/healthcheck",
    responses={
        status.HTTP_200_OK: {"description": "Healthcheck performed"}
    },
)
async def healthcheck():
    """
    Healthcheck endpoint
    """
    logger.info(f"app healthcheck performed")
    return Response(status_code=status.HTTP_200_OK)
