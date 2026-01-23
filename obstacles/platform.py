import pymunk
from obstacles.base_obstacle import BaseObstacle

class Platform(BaseObstacle):
    def __init__(self, space, x, y, w, h):
        super().__init__(space)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (w, h))
        self.shape.friction = 1.0
        space.add(self.body, self.shape)
