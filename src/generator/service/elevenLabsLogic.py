import requests
import os

from elevenlabs import set_api_key, generate, clone, voices, save
from service import utils


class ElevenLabsAPI:
    def __init__(self, apiKey):
        set_api_key(apiKey)
        self.apiKey = apiKey
        self.voiceModel = "eleven_multilingual_v2"

    def readTexts(self, text, voice) -> bytes:
        audio = generate(text=text, voice=voice, model=self.voiceModel)
        return audio

    def saveAudio(self, audio, path, filename) -> None:
        save(audio=audio, filename=os.path.join(path, "generated_" + filename) + ".mp3")

    def listVoices(self) -> list:
        vce = [(v.voice_id, v.name) for v in voices()]
        return vce

    def getNameByVoiceID(self, voice_id: str) -> str:
        vce = [(v.voice_id, v.name) for v in voices()]
        for voice in vce:
            if voice[0] == voice_id:
                return voice[1]
        return None

    def createOwnVoice(self, name, pathToVoicesDir, description) -> None:
        voicesMP3s = utils.get_files_from_dir(pathToVoicesDir)
        self.voice = clone(
            name=name,
            description=description,
            files=voicesMP3s,
        )

    def deleteVoice(self, voiceID: str) -> None:
        response = requests.delete(
            url=f"https://api.elevenlabs.io/v1/voices/{voiceID}",
            headers={"xi-api-key": self.apiKey},
        )
        if response.status_code != 200:
            raise Exception(f"Connection error: {response.status_code}, {response}")
