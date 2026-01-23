import pygame
from random import randint

from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from config.user_settings import NAMES, PHOTOS, NUM_MARBLES, PHOTOS, COLORS, SOUNDS

from core.world import World
from core.camera import Camera
from core.renderer import Renderer
from core.event_manager import EventManager

from entities.ball import Ball

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        
        self.world = World(screen=self.screen)
        self.camera = Camera(SCREEN_HEIGHT)
        self.renderer = Renderer(self.screen, self.camera)
        self.events = EventManager()

        # Create balls based on user settings
        self.balls = []
        for i in range(NUM_MARBLES):
            ball = Ball(self.world.space, 100 + i * 50, 50)
            ball.name = NAMES[i % len(NAMES)]
            ball.photo = PHOTOS[i % len(PHOTOS)]
            ball.color = COLORS[i % len(COLORS)]
            ball.sound = SOUNDS[i % len(SOUNDS)]
            self.balls.append(ball)

        self.level = None

    def load_level(self, level_cls):
        self.level = level_cls(self.world.space)
        self.level.build()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            running = self.events.process()

            self.world.space.step(dt)

            leader_y = max(ball.body.position.y for ball in self.balls)
            self.camera.update(leader_y)

            self.screen.fill((240, 240, 240))
            self.renderer.draw(self.world.space)
            pygame.display.flip()

        pygame.quit()