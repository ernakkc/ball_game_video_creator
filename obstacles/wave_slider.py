import pymunk
import math
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACLE_COLORS,
    OBSTACLE_COLORS_EDGE,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class WaveSlider(BaseObstacle):
    """Dalga gibi hareket eden yatay kaydırıcılar - 3 tane üst üste farklı fazlarda"""

    def __init__(self, space, x, y, width=200, height=20, amplitude=100, speed=10,
                 color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)

        self.time = 0
        
        if color is None:
            resolved = OBSTACLE_COLORS.get('slider')
        elif isinstance(color, str):
            resolved = OBSTACLE_COLORS.get(color, OBSTACLE_COLORS.get('slider'))
        else:
            resolved = color

        rgba = to_rgba_float(resolved)
        edge_rgba = to_rgba_float(OBSTACLE_COLORS_EDGE.get('slider', resolved))

        self.sliders = []
        self.initial_x = x
        self.amplitude = amplitude
        self.speed = speed
        self.time = 0

        # 3 tane slider oluştur, her biri farklı fazda
        for i in range(3):
            body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            body.position = x, y + i * 60  # Alt alta 60 birim aralıkla

            shape = pymunk.Poly.create_box(body, (width, height))
            shape.friction = OBSTACLE_FRICTION
            shape.elasticity = ELASTICITY
            shape.color = rgba
            shape.edge_color = edge_rgba

            space.add(body, shape)
            self.sliders.append((body, shape))

    def update(self, dt):
        """Sliderları güncelle - dalga hareketi"""
        self.time += dt

        for i, (body, shape) in enumerate(self.sliders):
            # Her slider farklı fazda hareket etsin
            phase = i * (2 * math.pi / 3)  # 120 derece faz farkı
            offset = self.amplitude * math.sin(self.speed * self.time + phase)
            body.position = (self.initial_x + offset, body.position.y)
            body.velocity = (self.amplitude * self.speed * math.cos(self.speed * self.time + phase), 0)

    def get_height(self):
        return 180  # 3 slider * 60 aralık</content>
