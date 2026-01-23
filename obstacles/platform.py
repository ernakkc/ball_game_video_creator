import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import OBSTACLE_COLORS, OBSTACLE_COLORS_EDGE, DEFAULT_OBSTACLE_COLOR, ELASTICITY, OBSTACLE_FRICTION
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
        if color is None: resolved = OBSTACLE_COLORS.get('platform')
        elif isinstance(color, str): resolved = OBSTACLE_COLORS.get(color, OBSTACLE_COLORS.get('platform'))
        else: resolved = color
        self.shape.color = to_rgba_float(resolved)
        self.shape.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('platform', resolved))
        
        space.add(self.body, self.shape)
        
        self.height = h
    
    def get_height(self):
        return self.height + 100
