from Regional import Regional

class Region(Regional):
    name: str

    def __init__(self, name, rm, p, gs):
        self.name = name
        super().__init__(rm, p, gs)