from util.file_operations import load_json_from_file

class GlobalAttributes:
    def __init__(self, file_name):
        self.load_data_files(file_name)
    
    def load_data_files(self, file_name):
        data = load_json_from_file(file_name)
        self.time_duration = data["time_duration"]
        self.time_step = data["time_step"]
        self.standard_radio_radius = data["standard_radio_radius"]