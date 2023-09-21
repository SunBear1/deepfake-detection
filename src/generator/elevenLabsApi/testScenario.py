import elevenLabsApi


APIKEY = "<APIKEY>"

testAPI = elevenLabsApi.ElevenLabsAPI(apiKey=APIKEY)

testAPI.createOwnVoice(name="WWHITE", pathToVoicesDir="<VOICESDIR>", description="test")

print(testAPI.listVoices)

testAPI.readTexts(pathToTextsFile="<TEXTSFILE>", pathToSavefilesDir="<SAVEFILESDIR>", baseFilename="WWhiteTestSpeech")

testAPI.deleteVoice