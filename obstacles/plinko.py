import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import OBSTACLE_COLORS, OBSTACLE_COLORS_EDGE, DEFAULT_OBSTACLE_COLOR, ELASTICITY, OBSTACLE_FRICTION, OBSTACLE_DENSITY, OBSTACLE_RADIUS, DEFAULT_OBSTACLE_MASS, PLINKO_SPACING_X, PLINKO_SPACING_Y, MAX_OBSTACLE_HEIGHT
from utils.color_utils import to_rgba_float

class Plinko(BaseObstacle):
    def __init__(self, space, x, y, x_count, y_count, angle=0, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        self.y_count = y_count
        for i in range(x_count):
            for j in range(y_count):
                peg_x = x + i * PLINKO_SPACING_X + (j % 2) * (PLINKO_SPACING_X / 2)
                peg_y = y + j * PLINKO_SPACING_Y

                if peg_x < 0 or peg_x > 2000 or peg_y > MAX_OBSTACLE_HEIGHT:
                    continue  # Skip pegs outside the desired range

                self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
                self.body.position = peg_x, peg_y
                self.shape = pymunk.Circle(self.body, OBSTACLE_RADIUS)

                self.shape.friction = OBSTACLE_FRICTION
                self.shape.elasticity = ELASTICITY

                # COLOR RESOLUTION 
                if color is None: resolved = OBSTACLE_COLORS.get('plinko')
                elif isinstance(color, str): resolved = OBSTACLE_COLORS.get(color, OBSTACLE_COLORS.get('plinko'))
                else: resolved = color
                self.shape.color = to_rgba_float(resolved)
                self.shape.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('plinko', resolved))
                
                space.add(self.body, self.shape)
    
    def get_height(self):
        return self.y_count * PLINKO_SPACING_Y + 150