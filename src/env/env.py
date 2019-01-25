import pygame, random
from src.env.entity import Entity

from hashlib import md5

from math import radians, cos, sin

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3

ACTION_LOOKUP = {
    LEFT: pygame.K_LEFT,
    RIGHT: pygame.K_RIGHT,
    DOWN: pygame.K_DOWN,
    UP: pygame.K_UP
}


class Environment:
    def __init__(self, dimensions=(50, 50), scale=1, render=False, keyboard=False, seed=0):
        self.dimensions = (dimensions[0] * scale, dimensions[1] * scale)

        self.background = None

        self.scale = scale

        self.render = render
        self.keyboard = keyboard
        self.screen = None
        self.finished = False

        self.player = Entity(x=self.dimensions[0] / 2, y=self.dimensions[1] / 2, size=scale)
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.fov_size = 50

        self.fitness = 0

        self.projectiles = []

        random.seed(seed)

        self.spawn_segments = [ ((0, -self.player.size), (self.dimensions[0] - self.player.size, -self.player.size), (0, 180)),\
                                ((-self.player.size, 0), (-self.player.size, self.dimensions[1] - self.player.size), (-90, 90)), \
                                ((0, self.dimensions[1] + self.player.size), \
                                 (self.dimensions[0] - self.player.size, self.dimensions[1] + self.player.size), (180, 360)), \
                                ((self.dimensions[0] + self.player.size, 0), (self.dimensions[0] + self.player.size, \
                                                                              self.dimensions[1] - self.player.size), (90, 180)) ]

        self.valid_keys = { pygame.K_LEFT : 'left', pygame.K_RIGHT: 'right', pygame.K_DOWN: 'down', pygame.K_UP: 'up' }

        self._initialize_render()

    def _handle_events(self):
        for event in pygame.event.get():
            self._handle_event(event)

    def _initialize_render(self):
        if self.render:
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.dimensions)

        self.background = pygame.Surface(self.dimensions)
        self.background.fill((255, 255, 255))

    """ Crop the original full-background image and return the raster """
    @property
    def raster(self):
        fov = pygame.Surface((self.fov_size, self.fov_size))
        fov.blit(self.background, (0, 0), (self.dimensions[0] / 2 - self.fov_size, \
                                           self.dimensions[1] / 2 - self.fov_size, \
                                           self.dimensions[0] / 2 + self.fov_size, \
                                           self.dimensions[1] / 2 + self.fov_size))
        return fov.get_buffer()

    def reset_keys(self):
        for key in self.valid_keys.values():
            setattr(self, key, False)

    def _set_key(self, key, state):
        if key in self.valid_keys:
            setattr(self, self.valid_keys[key], state)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.finished = True
        elif event.type == pygame.KEYDOWN:
            self._set_key(event.key, True)
        elif event.type == pygame.KEYUP:
            self._set_key(event.key, False)

    def _handle_player_movement(self):
        if self.left:
            self.player.x -= 1

        if self.right:
            self.player.x += 1

        if self.down:
            self.player.y += 1

        if self.up:
            self.player.y -= 1

    @property
    def hash(self):
        m = md5()
        m.update(self.raster)
        return m.hexdigest()

    def take_action(self, action):
        if action in ACTION_LOOKUP:
            self._set_key(ACTION_LOOKUP[action], True)
        self._tick()

    # Spawn an entity
    def _spawn_projectile(self):
        if len(self.projectiles) < 200:
            segment = random.choice(self.spawn_segments)
            pos = (random.uniform(segment[0][0], segment[1][0]), random.uniform(segment[0][1], segment[1][1]))
            angle = radians(random.randint(segment[2][0], segment[2][1]))
            dir = (cos(angle), sin(angle))
            self.projectiles.append(Entity(x=pos[0], y=pos[1], size=self.scale, vx=dir[0], vy=dir[1]))

    def render_entity(self, entity):
        if self.player:
            pygame.draw.rect(self.background, (0, 0, 0),
                         (entity.position[0] - self.player.x + self.dimensions[0] / 2,
                          entity.position[1] - self.player.y + self.dimensions[1] / 2, entity.size, entity.size))

    def _render_projectiles(self):
        for entity in self.projectiles:
            self.render_entity(entity)

    def _move_projectiles(self):
        to_remove = []
        for entity in self.projectiles:
            entity.update()

            if self.player and entity.collides(self.player):
                self.player = None
                self.finished = True

            if entity.should_delete:
                to_remove.append(entity)

        for entity in to_remove:
            self.projectiles.remove(entity)

    def _tick(self):
        self.background.fill((255, 255, 255))

        if self.player:
            self._handle_player_movement()
            pygame.draw.rect(self.background, (255, 0, 0), (self.dimensions[0] / 2, self.dimensions[1] / 2, \
                                                            self.player.size, self.player.size))
            self.fitness += 1

        self._move_projectiles()
        self._render_projectiles()

        self._spawn_projectile()

    def run(self):
        while not self.finished:
            if self.keyboard and self.render:
                self._handle_events()

            if self.render:
                self.screen.blit(self.background, (0, 0))

            self._tick()

            if self.render:
                pygame.display.flip()
                pygame.time.wait(25)
