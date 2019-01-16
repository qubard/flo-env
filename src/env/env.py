import pygame
from src.entity import Entity

from hashlib import md5

class Environment:
    def __init__(self, dimensions=(500, 500), render=False, keyboard=False):
        self.dimensions = dimensions
        self.render = render
        self.keyboard = keyboard
        self.screen = None
        self.shouldRun = True

        self.player = Entity(x=dimensions[0] / 2, y=dimensions[1] / 2, size=30)
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.projectiles = []

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
        m = md5()
        m.update(self.background.get_buffer())
        return m.hexdigest()

    # Spawn an entity
    def _spawn_projectile(self):
        self.projectiles.append(Entity(x=50, y=50, size=25, vx=1, vy=1))

    def _render_projectiles(self):
        for entity in self.projectiles:
            pygame.draw.rect(self.background, (0, 0, 0),
                             (entity.position[0], entity.position[1], entity.size, entity.size))

    def _move_projectiles(self):
        for entity in self.projectiles:
            entity.update()

    def run(self):
        if self.render:
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.dimensions)

        self.background = pygame.Surface(self.dimensions)
        self.background.fill((255, 255, 255))

        self._spawn_projectile()

        while self.shouldRun:
            if self.keyboard and self.render:
                self.handle_events()

            if self.render:
                self.screen.blit(self.background, (0, 0))

            self.background.fill((255, 255, 255))

            pygame.draw.rect(self.background, (255, 0, 0), (self.player.position[0], self.player.position[1], self.player.size, self.player.size))

            self._move_projectiles()
            self._render_projectiles()

            self.handle_player_movement()

            print(self.state_hash())

            if self.render:
                pygame.display.flip()
            pygame.time.wait(25)
