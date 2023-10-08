class Town:
    town_id: int
    name: str

    def __init__(self, town_id, name):
        self.town_id = town_id
        self.name = name
        self.regions = []
    
    def add_region(self, region):
        self.regions.append(region)
