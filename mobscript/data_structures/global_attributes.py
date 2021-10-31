import pathlib
from ..util.file_operations import load_json_from_file

class GlobalAttributes:
    def __init__(self, file_name: pathlib.Path) -> None:
        self.load_data_files(pathlib.Path(file_name))
    
    def load_data_files(self, file_name: pathlib.Path) -> None:
        data = load_json_from_file(pathlib.Path(file_name))
        self.time_duration = data["time_duration"]
        self.time_step = data["time_step"]
        self.standard_radio_radius = data["standard_radio_radius"]
        self.length_to_pixels = data["length_to_pixels"]