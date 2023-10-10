import os

import requests

PATH_TO_SOURCES_DIRECTORY = os.getenv("PATH_TO_SOURCES")
URL = "http://projektbadawczyserver.eastus2.cloudapp.azure.com/api/v1"


def prepare_text_file(path_to_file: str) -> str:
    with open(path_to_file, "r") as f:
        text = f.readlines()
    without_end_line_character = [element.replace("\n", "") for element in text]
    with_ending_character = [element + "." for element in without_end_line_character]
    without_idx_number = [element.split(" ", 1)[1] for element in with_ending_character]
    return " ".join(without_idx_number)


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


def generate_deepfake_from_existing_voice(voice_id: str, text: str) -> None:
    print(f"Generating deepfake from voice with id: {voice_id}")
    response = requests.put(
        url=f"{URL}/voice/{voice_id}",
        data={"text": text},
    )
    if response.status_code != 200:
        raise Exception(f"Error occurred during generating deepfake from voice with id {voice_id}. Error: {response}")
    print(f"Deepfake from voice with id {voice_id} generated successfully. Voice has been saved in Azure storage "
          f"container.")


if __name__ == "__main__":
    for file in os.listdir(PATH_TO_SOURCES_DIRECTORY):
        if file.endswith(".txt"):
            print(f"Processing file: {file}")
            text_to_speak = prepare_text_file(path_to_file=os.path.join(PATH_TO_SOURCES_DIRECTORY, file))
            created_voice_id = create_new_voice(
                path_to_voice_file=os.path.join(PATH_TO_SOURCES_DIRECTORY, file.replace('.trans.txt', '.flac')))
            generate_deepfake_from_existing_voice(voice_id=created_voice_id, text=text_to_speak)
            delete_old_voice(old_voice_id=created_voice_id)
