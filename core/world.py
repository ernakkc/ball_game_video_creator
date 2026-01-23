import pymunk
from config.settings import GRAVITY

class World:
    def __init__(self, screen):
        self.screen = screen
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        