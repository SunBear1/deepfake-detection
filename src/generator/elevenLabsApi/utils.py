import os


def fileTXT_to_list(filenameAndFilepath):
    with open(filenameAndFilepath, 'r') as file:
        content = file.read()
        lines = content.split(';')
        lines = [line.strip() for line in lines if line.strip()]


    return [element.replace("\n", "") for element in lines]
    
def getMP3_from_dir(MP3directory):
    mp3_files = [os.path.join(MP3directory, f) for f in os.listdir(MP3directory) if f.endswith('.mp3')]


    return mp3_files