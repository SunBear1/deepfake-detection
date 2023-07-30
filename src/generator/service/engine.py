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

    def download_audio_file(self):
        """
        Download audio file
        """
        self.azure_client.download_file()
        logger.info("Downloading audio file")
        return "audio_file"

    def upload_audio_file(self, audio_df_file):
        """
        Upload audio file
        """
        self.azure_client.upload_file()
        logger.info("Uploading audio file")

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
