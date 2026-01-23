import pygame

class EventManager:
    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
