import pygame


class Environment:
    def __init__(self, dimensions=(1024,768)):
        self.dimensions = dimensions
        self.screen = None
        self.shouldRun = True

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.shouldRun = False

    def run(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.dimensions)
        while self.shouldRun:
            self.handle_events()
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, 50, 50))

            pygame.display.flip()
            pygame.time.wait(1)
