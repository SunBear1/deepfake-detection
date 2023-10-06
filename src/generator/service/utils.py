import os


def file_content_to_list(file_path: str) -> list:
    with open(file_path, 'r') as file:
        content = file.read()
        lines = content.split(';')
        lines = [line.strip() for line in lines if line.strip()]

    return [element.replace("\n", "") for element in lines]


def get_all_files_from_dir(directory_name: str) -> list:
    file_paths = [os.path.join(directory_name, f) for f in os.listdir(directory_name)]

    return file_paths
