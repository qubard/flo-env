import pygame
from src.entity import Entity

from hashlib import sha256

class Environment:
    def __init__(self, dimensions=(500, 500), render=True):
        self.dimensions = dimensions
        self.render = render
        self.screen = None
        self.shouldRun = True
        self.player = Entity(x=dimensions[0] / 2, y=dimensions[1] / 2, size=30)
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.valid_keys = { pygame.K_LEFT : 'left', pygame.K_RIGHT: 'right', pygame.K_DOWN: 'down', pygame.K_UP: 'up' }

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.shouldRun = False
        elif event.type == pygame.KEYDOWN:
            if event.key in self.valid_keys:
                key = self.valid_keys[event.key]
                setattr(self, key, True)
        elif event.type == pygame.KEYUP:
            if event.key in self.valid_keys:
                key = self.valid_keys[event.key]
                setattr(self, key, False)

    def handle_player_movement(self):
        if self.left:
            self.player.x -= 1

        if self.right:
            self.player.x += 1

        if self.down:
            self.player.y += 1

        if self.up:
            self.player.y -= 1

    def state_hash(self):
        m = sha256()
        m.update(self.background.get_buffer())
        return m.digest()

    def run(self):
        #pygame.display.init()
        #self.screen = pygame.display.set_mode(self.dimensions)
        self.background = pygame.Surface(self.dimensions)
        self.background.fill((255, 255, 255))
        while self.shouldRun:
            #self.handle_events()
            #self.screen.blit(background, (0, 0))
            self.background.fill((255, 255, 255))

            pygame.draw.rect(self.background, (255, 0, 0), (self.player.position[0], self.player.position[1], self.player.size, self.player.size))

            self.handle_player_movement()

            print(self.state_hash())

            self.left = True

            #pygame.display.flip()
            pygame.time.wait(1000)
