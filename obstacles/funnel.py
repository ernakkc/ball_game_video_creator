import pymunk
import math
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACKLE_COLORS,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
)
from utils.color_utils import to_rgba_float


class Funnel(BaseObstacle):
    """Huni şekli - topları merkeze yönlendirir"""
    def __init__(self, space, y):
        super().__init__(space)

        # Sol üst
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = 135, y
        self.body.angle = 30 * (3.14159 / 180)  # Convert angle to radians
        self.shape = pymunk.Poly.create_box(self.body, (400, 30))
        self.shape.friction = OBSTACLE_FRICTION
        self.shape.elasticity = ELASTICITY
        self.shape.color = to_rgba_float(OBSTACKLE_COLORS.get('funnel'))
        space.add(self.body, self.shape)

        # Sağ üst
        self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body2.position = 400, y + 160
        self.body2.angle = -30 * (3.14159 / 180)  # Convert angle to radians
        self.shape2 = pymunk.Poly.create_box(self.body2, (400, 30))
        self.shape2.friction = OBSTACLE_FRICTION
        self.shape2.elasticity = ELASTICITY
        self.shape2.color = to_rgba_float(OBSTACKLE_COLORS.get('funnel'))
        space.add(self.body2, self.shape2)

        # Alt sol
        self.body3 = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body3.position = 135, y + 320
        self.body3.angle = 30 * (3.14159 / 180)  # Convert angle to radians
        self.shape3 = pymunk.Poly.create_box(self.body3, (400, 30))
        self.shape3.friction = OBSTACLE_FRICTION
        self.shape3.elasticity = ELASTICITY
        self.shape3.color = to_rgba_float(OBSTACKLE_COLORS.get('funnel'))
        space.add(self.body3, self.shape3)

        # Alt sağ
        self.body4 = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body4.position = 400, y + 480
        self.body4.angle = -30 * (3.14159 / 180)  # Convert angle to radians
        self.shape4 = pymunk.Poly.create_box(self.body4, (400, 30))
        self.shape4.friction = OBSTACLE_FRICTION
        self.shape4.elasticity = ELASTICITY
        self.shape4.color = to_rgba_float(OBSTACKLE_COLORS.get('funnel'))
        space.add(self.body4, self.shape4)