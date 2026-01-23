import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import OBSTACKLE_COLORS, DEFAULT_OBSTACLE_COLOR, ELASTICITY, OBSTACLE_FRICTION
from utils.color_utils import to_rgba_float

class Platform(BaseObstacle):
    def __init__(self, space, x, y, w, h, angle=0, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.body.angle = angle * (3.14159 / 180)  # Convert angle to radians
        self.shape = pymunk.Poly.create_box(self.body, (w, h))
        self.shape.friction = OBSTACLE_FRICTION
        self.shape.elasticity = ELASTICITY

        # COLOR RESOLUTION 
        if color is None: resolved = OBSTACKLE_COLORS.get('platform')
        elif isinstance(color, str): resolved = OBSTACKLE_COLORS.get(color, OBSTACKLE_COLORS.get('platform'))
        else: resolved = color
        self.shape.color = to_rgba_float(resolved)
        
        space.add(self.body, self.shape)
