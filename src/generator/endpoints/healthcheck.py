import logging

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from service.azure_client import AzureStorageClient

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
    az_client = AzureStorageClient()
    if az_client.blob_service_client.get_container_client("deepfake-audio-dataset").exists():
        return Response(status_code=status.HTTP_200_OK, content="I'm healthy")
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Can't connect to Azure container")
