import json
from pathlib import Path


def create_blank_file(directory, file_name):
    Path("generated_data").mkdir(parents=True, exist_ok=True)
    full_path = directory + "/" + file_name
    file_path = Path(full_path)
    if file_path.is_file() is False:
        with open(full_path, "w") as outfile:
            template = {}
            json.dump(template, outfile)


def load_json_from_file(directory, file_name):
    with open(directory + "/" + file_name) as json_file:
        return json.load(json_file)
