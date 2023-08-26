import logging

from service.azure_client import AzureStorageClient

logger = logging.getLogger("generator")


class Engine:
    """
   Generator engine class
    """
    mail_address = None
    mail_password = None
    azure_client = AzureStorageClient()

    def download_audio_file(self, blob_name: str, container_name: str = "raw-audio-dataset") -> bytes:
        """
        Download audio file
        """
        logger.info(f"Downloading {blob_name} audio file from container {container_name}")
        return self.azure_client.download_file(container_name=container_name, blob_name=blob_name)

    def upload_audio_file(self, blob_name: str, audio_df_file: bytes, blob_directory: str,
                          container_name: str = "deepfake-audio-dataset") -> None:
        """
        Upload audio file
        """
        blob_path = f"{blob_directory}/{blob_name}"
        logger.info(f"Uploading audio file to blob {blob_path} in container {container_name}")
        self.azure_client.upload_file(container_name=container_name, blob_name=blob_path,
                                      audio_file=audio_df_file)

    def get_current_file_id(self) -> str:
        """
        Get current id of a file
        :return:
        """
        logger.info("Getting current file id")
        number_of_files = self.azure_client.count_files(container_name="deepfake-audio-dataset",
                                                        directory_name="deepfakes") + 1
        return f"{number_of_files:05}"

    def create_temp_mail_account(self):
        """
        Create temporary mail account
        """
        self.mail_address = "ken@barbieland.com"
        self.mail_password = "mojodojocasahouse"
        logger.info("Creating temporary mail account")

    def generate_fake_audio_corentinj(self):
        """
        Generate fake audio using corentinj
        """
        logger.info("Generating fake audio using corentinj")

    def generate_fake_audio_elevenlabs(self, audio_file):
        """
        Generate fake audio using elevenlabs
        """
        logger.info("Generating fake audio using elevenlabs")
        return "audio_df_file"

    def generate_fake_audio_fakeyou(self):
        """
        Generate fake audio using fakeyou
        """
        logger.info("Generating fake audio using fakeyou")
