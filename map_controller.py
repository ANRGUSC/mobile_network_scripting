from util.file_operations import load_json_from_file

class MapController:
    map = []

    def load_map(self, file_name):
        json = load_json_from_file(file_name)
        self.scale = json["metadata"]["scale"]

        map = json["map"]
        self.row_size = len(map)
        self.col_size = map[0]
        self.length = len(map[0])

    def convert_waypoints_to_path(self, waypoints):
        return waypoints