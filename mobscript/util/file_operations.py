import json
import pathlib
from typing import Union, Dict, List

def create_blank_file(full_path: pathlib.Path) -> None:
    full_path.parent.mkdir(exist_ok=True, parents=True)
    full_path.write_text(json.dumps({}))

def load_json_from_file(file_name: pathlib.Path) -> Union[Dict, List]:
    return json.loads( pathlib.Path(file_name).read_text())
