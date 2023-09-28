from elevenlabs import set_api_key, generate, clone, voices, save
import requests
import utils
import os


class ElevenLabsAPI:
    def __init__(self, apiKey):
        set_api_key(apiKey)
        self.apiKey = apiKey
        self.voice = ""
        # Can be only english with parameter: eleven_monolingual_v1
        self.voiceModel = "eleven_multilingual_v2" 

    def readTexts(self, pathToTextsFile, pathToSavefilesDir, baseFilename) -> None:
        texts = utils.fileTXT_to_list(pathToTextsFile)
        if self.voice == None:
            raise Exception(f'No voice in variable self.voice: {self.voice}')
        for text in texts:
            audio = generate(
                text = text,
                voice = self.voice,
                model = self.voiceModel
            )
            save(
                audio=audio,
                filename = os.path.join(pathToSavefilesDir,baseFilename) + ".mp3"
            )
    
    def listVoices(self) -> list:
        vce = [(v.voice_id, v.name) for v in voices()]
        return vce      

    def setVoice(self, voice) -> None: 
        self.voice = voice

    def createOwnVoice(self, name, pathToVoicesDir, description) -> None:
        voicesMP3s = utils.getMP3_from_dir(pathToVoicesDir)
        self.voice = clone(
            name=name,
            description=description,
            files=voicesMP3s,
        )
    def getVoice(self):
        return self.voice
    
    def deleteVoice(self) -> None:
        if self.voice == "":
            raise Exception(f'No voice in variable self.voice, no voice has been deleted: {self.voice}')
        response = requests.delete(url='https://api.elevenlabs.io/v1/voices/{self.voice.id}', headers={'xi-api-key': self.apiKey})
        if response.status_code != 200:
            raise Exception(f'Connection error: {response.status_code}, {response}')
        