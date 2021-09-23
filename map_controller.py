from util.file_operations import load_json_from_file

class MapController:
    cellular_zones = []

    def load_map(self, file_name):
        json = load_json_from_file(file_name)
        self.scale = json["metadata"]["scale"]
        self.map = json["map"]
        self.row_size = len(self.map)
        self.col_size = self.map[0]
        self.length = len(self.map[0])

    def add_cellular_zone(self, cellular_zone):
        self.cellular_zones.append(cellular_zone)

    def get_cellular_zones(self):
        return self.cellular_zones

    def convert_waypoints_to_path(self, waypoints, allowable_terrain):
        print(allowable_terrain, waypoints)
        return waypoints

