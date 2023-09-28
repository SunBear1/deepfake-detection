import elevenLabsLogic

APIKEY = "a8412809ee48754b006d19396dd7eb40"

testAPI = elevenLabsLogic.ElevenLabsAPI(apiKey=APIKEY)

testAPI.createOwnVoice(name="WWHITE", pathToVoicesDir="C:\\Users\\kubas\\Desktop\\testVoices", description="test")

print(testAPI.listVoices)
testAPI.setVoice(testAPI.listVoices)

testAPI.readTexts(pathToTextsFile="C:\\Users\\kubas\\Desktop\\test.txt", pathToSavefilesDir="C:\\Users\\kubas\\Desktop\\testResults", baseFilename="WWhiteTestSpeech")

testAPI.deleteVoice