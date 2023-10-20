import os
from pydub import AudioSegment
import soundfile as sf
import numpy as np
from time import sleep

import requests

# PATH_TO_SOURCES_DIRECTORY = os.getenv("PATH_TO_SOURCES")
URL = "http://projektbadawczyserver.eastus2.cloudapp.azure.com/api/v1"


def prepare_text_file(path_to_file: str) -> str:
    with open(path_to_file, "r") as f:
        text = f.readlines()
    without_end_line_character = [element.replace("\n", "") for element in text]
    with_ending_character = [element + "." for element in without_end_line_character]
    without_idx_number = [element.split(" ", 1)[1] for element in with_ending_character]
    return " ".join(without_idx_number)

def prepare_text_file_V2(path_to_file: str) -> str:
    parts_pairs = []
    with open(path_to_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                number, text = parts
                number = number.replace('-', '/') 
                print(number)
                parts_pairs.append((number, text))
    return parts_pairs

def create_new_voice(path_to_voice_file: str) -> str:
    print(f"Creating a clone of a voice from file {path_to_voice_file}")
    response = requests.post(
        url=f"{URL}/voices",
        files={"file": open(path_to_voice_file, "rb")},
    )
    if response.status_code != 201:
        raise Exception(f"Error occurred during creating a clone of a voice from file {path_to_voice_file}. "
                        f"Error: {response}")
    voice_id = response.content.decode("utf-8").split(" ")[-1]
    print(f"Voice {path_to_voice_file} created successfully with ID {voice_id}")
    return voice_id


def delete_old_voice(old_voice_id: str) -> None:
    print(f"Deleting voice with id: {old_voice_id}")
    response = requests.delete(
        url=f"{URL}/voice/{old_voice_id}",
    )
    if response.status_code != 204:
        raise Exception(f"Error occurred during deleting voice with id {old_voice_id}. Error: {response}")
    print(f"Voice with id {old_voice_id} deleted successfully")


def generate_deepfake_from_existing_voice(voice_id: str, subdir: str, text: str) -> None:
    print(f"Generating deepfake from voice with id: {voice_id}")
    response = requests.put(
        url=f"{URL}/voice/{voice_id}",
        json={"subdir":subdir, "text": text},
    )
    if response.status_code != 200:
        print(f"Error occurred during generating deepfake from voice with id {voice_id}. Error: {response}")
        sleep(15)
    print(f"Deepfake from voice with id {voice_id} generated successfully. Voice has been saved in Azure storage "
          f"container.")

def merge_flac_files(directory_path, output_file):
    flac_files = [f for f in os.listdir(directory_path) if f.endswith(".flac")]
    
    if not flac_files:
        print(f"No FLAC files found in {directory_path}.")
        return
    
    audio_data = []
    for file in flac_files:
        audio_path = os.path.join(directory_path, file)
        data, sample_rate = sf.read(audio_path)
        audio_data.append(data)
    
    concatenated_audio = np.concatenate(audio_data)
    sf.write(output_file, concatenated_audio, sample_rate)
    print(f"Merged {len(flac_files)} FLAC files into {output_file}.")

if __name__ == "__main__":
    PATH_TO_SOURCES_DI0RECTORY = "<INSERT PATH HERE>"
    for dir in os.listdir(PATH_TO_SOURCES_DI0RECTORY):
        dir = PATH_TO_SOURCES_DI0RECTORY + os.sep + dir
        if os.path.isdir(dir):
            for subdir in os.listdir(dir):
                subdir = dir + os.sep + subdir
                for file in os.listdir(subdir):
                    if file.endswith(".txt"):
                        print(f"Processing file: {file}")
                        combinedFlacFileMerged = subdir + os.sep + "MERGED_" + file.replace('.trans.txt', '.flac')
                        merge_flac_files(directory_path=subdir, output_file=combinedFlacFileMerged)
                        text_to_speak_pairs = prepare_text_file_V2(path_to_file=os.path.join(subdir, file))
                        created_voice_id = create_new_voice(
                            path_to_voice_file=combinedFlacFileMerged)
                        for text_chunk in text_to_speak_pairs:
                            print(text_chunk)
                            generate_deepfake_from_existing_voice(voice_id=created_voice_id, subdir=text_chunk[0] , text=text_chunk[1])
                            sleep(1.5)
                        delete_old_voice(old_voice_id=created_voice_id)
                        os.remove(combinedFlacFileMerged)
                        print(f"{combinedFlacFileMerged} has been successfully deleted.")
