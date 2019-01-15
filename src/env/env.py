import pygame
import time


class Environment:
    def __init__(self, dimensions=(1024,768)):
        self.dimensions = dimensions
        self.screen = None

    def run(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.dimensions)
        while True:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, 50, 50))

            pygame.display.flip()
            time.sleep(1)
