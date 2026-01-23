import math
import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACLE_COLORS,
    OBSTACLE_COLORS_EDGE,
    DEFAULT_OBSTACLE_COLOR,
    OBSTACLE_FRICTION,
    ELASTICITY,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class LuckyCup(BaseObstacle):
    def __init__(
        self,
        space,
        x,
        y
    ):
        super().__init__(space)

        x = x + 155  # Merkeze al

        for y_count in range(5):
            for x_count in range(3):
                peg_x = x + x_count * 165
                peg_y = y + y_count * 150

                # zikzaklı yerleştirme
                if y_count % 2 == 0:
                    peg_x -= 80

                if peg_x < 0 or peg_x > 2000 or peg_y > MAX_OBSTACLE_HEIGHT:
                    continue  # Skip pegs outside the desired range
                
                
                self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
                self.body.position = (peg_x, peg_y)
    
                start_ang, end_ang = math.pi, 0
                segments=40 
                radius=80

                points = []
                for i in range(segments + 1):
                    t = i / segments
                    ang = start_ang + (end_ang - start_ang) * t
                    px = math.cos(ang) * radius
                    py = math.sin(ang) * radius
                    points.append((px, py))

                color = OBSTACLE_COLORS.get('lucky_cup')

                self.segments = []
                half_gap = 70 / 2

                for a, b in zip(points[:-1], points[1:]):
                    if abs(a[0]) < half_gap and abs(b[0]) < half_gap:
                        continue

                    seg = pymunk.Segment(self.body, a, b, 2)
                    seg.friction = OBSTACLE_FRICTION
                    seg.elasticity = ELASTICITY
                    seg.color = to_rgba_float(color=color)
                    seg.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('lucky_cup', color))
                    self.segments.append(seg)

                space.add(self.body, *self.segments)
    
    def get_height(self):
        return 5 * 150 + 200  # 5 rows of cups plus spacing
