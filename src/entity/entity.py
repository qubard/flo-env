import pygame

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def position(self):
        return (self.x, self.y)
