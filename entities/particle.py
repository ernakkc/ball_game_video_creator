import pymunk
from entities.base_entity import BaseEntity
from config.settings import BALL_SIZE, BALL_MASS

class Particle(BaseEntity):
    def __init__(self, space, x, y, vx, vy, lifetime=10, size=3, color=(255, 255, 255)):
        super().__init__(space)
        self.body = pymunk.Body(0.1, pymunk.moment_for_circle(0.1, 0, size))
        self.body.position = x, y
        self.body.velocity = vx, vy
        
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = color
        self.shape.sensor = True  # Particles don't collide
        
        space.add(self.body, self.shape)
        
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.color = color
    
    def update(self, dt):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.space.remove(self.body, self.shape)
            return False
        # Renk soluklaş
        alpha = self.lifetime / self.max_lifetime
        self.shape.color = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha),
            255
        )
        return True