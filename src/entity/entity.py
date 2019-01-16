class Entity:
    def __init__(self, x, y, size, vx=0, vy=0):
        self.x = x
        self.y = y
        self.size = size
        self.vx = vx
        self.vy = vy

    @property
    def position(self):
        return (int(self.x), int(self.y))

    def collides(self, other):
        if self.x > other.x + other.size or other.x > self.x + self.size:
            return False

        if self.y > other.y + other.size or other.y > self.y + self.size:
            return False

        return True

    def update(self):
        self.x += self.vx
        self.y += self.vy