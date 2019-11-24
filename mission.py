class Mission:
    """
        An easy way to store rocket launches
    """
    def __init__(self, mission_name, location, lsp, rocket_name, date, start_time, end_time):
        self.mission_name = mission_name
        self.location = location
        self.lsp = lsp
        self.rocket_name = rocket_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def to_string(self):
        return "Mission [ Name: " + str(self.mission_name) \
               + ", Location: " + str(self.location) \
               + ", LSP: " + str(self.lsp) \
               + ", Rocket: " + str(self.rocket_name) \
               + ", Date: " + str(self.date) \
               + ", Start: " + str(self.start_time) \
               + ", End: " + str(self.end_time)
