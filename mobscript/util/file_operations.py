import json
from pathlib import Path

def create_blank_file(full_path):
    directory = full_path[:full_path.rindex('/')]
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_path = Path(full_path)
    if file_path.is_file() is False:
        with open(full_path, "w") as outfile:
            template = {}
            json.dump(template, outfile)


def load_json_from_file(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)
