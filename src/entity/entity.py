class Entity:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    @property
    def position(self):
        return (int(self.x), int(self.y))
