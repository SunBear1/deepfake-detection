from typing import Optional

import requests
import os

from elevenlabs import set_api_key, generate, clone, voices, save
from service import utils


class ElevenLabsClient:
    def __init__(self, apiKey):
        set_api_key(apiKey)
        self.apiKey = apiKey
        self.voiceModel = "eleven_multilingual_v2"

    def read_text(self, text, voice) -> bytes:
        audio = generate(text=text, voice=voice, model=self.voiceModel)
        return audio

    def save_audio(self, audio, path, filename) -> None:
        save(audio=audio, filename=os.path.join(path, "generated_" + filename) + ".mp3")

    def list_voices(self) -> list:
        vce = [(v.voice_id, v.name) for v in voices()]
        return vce

    def get_voice_name_by_id(self, voice_id: str) -> Optional[str]:
        vce = [(v.voice_id, v.name) for v in voices()]
        for voice in vce:
            if voice[0] == voice_id:
                return voice[1]
        return None

    def get_voice_id_by_name(self, voice_name: str) -> Optional[str]:
        vce = [(v.voice_id, v.name) for v in voices()]
        for voice in vce:
            if voice[1] == voice_name:
                return voice[0]
        return None

    def create_voice(self, name, path_to_voices_dir, description) -> None:
        voice_files = utils.get_all_files_from_dir(path_to_voices_dir)
        self.voice = clone(
            name=name,
            description=description,
            files=voice_files,
        )

    def delete_voice(self, voice_id: str) -> None:
        response = requests.delete(
            url=f"https://api.elevenlabs.io/v1/voices/{voice_id}",
            headers={"xi-api-key": self.apiKey},
        )
        if response.status_code != 200:
            raise Exception(f"Connection error: {response.status_code}, {response}")
