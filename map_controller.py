from util.file_operations import load_json_from_file

class MapController:
    map = []
    cellular_zones = []

    def load_map(self, file_name):
        json = load_json_from_file(file_name)
        self.scale = json["metadata"]["scale"]

        map = json["map"]
        self.row_size = len(map)
        self.col_size = map[0]
        self.length = len(map[0])

    def convert_waypoints_to_path(self, waypoints):
        return waypoints

    def add_cellular_zone(self, cellular_zone):
        self.cellular_zones.append(cellular_zone)

    def get_cellular_zones(self):
        return self.cellular_zones