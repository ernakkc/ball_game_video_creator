import pymunk
from random import randint, choice
from obstacles.base_obstacle import BaseObstacle
from config.settings import OBSTACLE_COLORS, OBSTACLE_COLORS_EDGE, DEFAULT_OBSTACLE_COLOR, ELASTICITY, OBSTACLE_FRICTION, OBSTACLE_DENSITY, OBSTACLE_RADIUS, DEFAULT_OBSTACLE_MASS, PLINKO_SPACING_X, PLINKO_SPACING_Y, MAX_OBSTACLE_HEIGHT
from utils.color_utils import to_rgba_float

class Minefield(BaseObstacle):
    def __init__(self, space, x, y):
        super().__init__(space)
        
        for y_counter in range(8):
            for x_counter in range(20):
                mine_x = x + x_counter * 120
                mine_y = y + y_counter * 120

                # rasgele dağılım
                mine_x = randint(x + x_counter * 120 - 30, x + x_counter * 120 + 30)
                mine_y = randint(y + y_counter * 120 - 30, y + y_counter * 120 + 30)

                if mine_x < 0 or mine_x > 2000 or mine_y > MAX_OBSTACLE_HEIGHT:
                    continue  # Skip mines outside the desired range
                
                size = 15
                verts = [(-size, -size), (size, -size), (0, size)]  # Eşkenar üçgen
                self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                self.body.position = mine_x, mine_y
                self.body.angular_velocity = choice([5, -5, 7, -7, 10, -10, 12, -12, 14, -14, 16, -16, 18, -18])  # Yerinde dönme
                self.shape = pymunk.Poly(self.body, verts)
                self.shape.friction = OBSTACLE_FRICTION
                self.shape.elasticity = ELASTICITY
                self.shape.color = to_rgba_float(OBSTACLE_COLORS.get('minefield'))
                self.shape.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('minefield', OBSTACLE_COLORS.get('minefield')))
                space.add(self.body, self.shape)
    
    def get_height(self):
        return 8 * 120 + 100  # 8 rows of mines plus spacing

