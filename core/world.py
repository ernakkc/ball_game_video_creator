import pymunk
from config.settings import GRAVITY, SCREEN_HEIGHT

class World:
    def __init__(self, screen):
        self.screen = screen
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
    def update_obstacles_visibility(self, camera_y):
        """Kamera dışındaki engelleri pasif et (performans)"""
        for shape in self.space.shapes:
            if hasattr(shape.body, 'position'):
                y = shape.body.position.y
                # Kameradan 1000px dışındaysa farklı kategori (çarpışma hesaplanmaz)
                is_far = not (camera_y - 1000 < y < camera_y + SCREEN_HEIGHT + 1000)
                if is_far:
                    shape.filter = pymunk.ShapeFilter(categories=0b10)  # Farklı kategori = çarpışma yok
                else:
                    shape.filter = pymunk.ShapeFilter(categories=0b1)  # Normal kategori