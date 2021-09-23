from util.file_operations import load_json_from_file

class GlobalAttributes:
    def __init__(self):
        self.time_duration = 10
        self.time_step = 1
        self.standard_radio_radius = 3
    
    def load_data_files(self, file_name):
        data = load_json_from_file(file_name)
        print(data)