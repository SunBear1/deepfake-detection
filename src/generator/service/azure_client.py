import os

from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONNECTION_STRING = (f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};"
                           f"AccountKey={AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net")


class AzureStorageClient:
    if AZURE_STORAGE_ACCOUNT == "" or AZURE_STORAGE_KEY == "":
        raise Exception("Azure connection credentials are not set")
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=AZURE_CONNECTION_STRING)

    @classmethod
    def upload_file(cls, container_name: str, audio_file: bytes, blob_name: str):
        container_client = cls.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(audio_file)

    @classmethod
    def download_file(cls, container_name: str, blob_name: str) -> bytes:
        container_client = cls.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    @classmethod
    def count_files(cls, container_name: str, directory_name: str) -> int:
        container_client = cls.blob_service_client.get_container_client(container_name)
        return len(list(container_client.list_blobs(name_starts_with=directory_name))) - 1
