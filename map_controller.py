from util.file_operations import load_json_from_file

class MapController:
    metadata = {}
    map = []

    def load_map(self, file_name):
        json = load_json_from_file(file_name)