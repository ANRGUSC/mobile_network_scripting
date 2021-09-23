class Unit:
    def __init__(self, key, name, unit_type, starting_position=(0, 0), waypoints=[], has_standard_radio=False,
                 has_cellular_radio=False, has_satellite_link=False):
        self.key = key
        self.name = name
        self.unit_type = unit_type
        self.has_standard_radio = has_standard_radio
        self.has_cellular_radio = has_cellular_radio
        self.has_satellite_link = has_satellite_link
        self.starting_position = starting_position
        self.waypoints = waypoints
        self.waypoints_timeline = []

    def encode(self):
        return self.__dict__

    def set_equipment(self, unit, has_standard_radio, has_cellular_radio, has_satellite_link):
        self.has_standard_radio = has_standard_radio
        self.has_cellular_radio = has_cellular_radio
        self.has_satellite_link = has_satellite_link

    def initialize(self):
        self.waypoints_timeline.sort(key=lambda x: x["start_time"])
