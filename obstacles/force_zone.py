import pymunk
import math
import random
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


class ForceZone(BaseObstacle):
    """4 yönde itim kuvveti uygulayan şeffaf bölge - oklarla gösterilir"""

    def __init__(self, space, x, y, radius=100, force_strength=1800,
                 color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)

        # Debug: her zaman eklensin
        print(f"ForceZone ekleniyor: x={x}, y={y}, radius={radius}, strength={force_strength}")

        # Renk çözümü
        if color is None:
            resolved = OBSTACLE_COLORS.get('windmill')
        elif isinstance(color, str):
            resolved = OBSTACLE_COLORS.get(color, OBSTACLE_COLORS.get('windmill'))
        else:
            resolved = color

        # Hangi yönde iteceği - rastgele seç veya parametreyle verildi
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        # Direction renkleri
        dir_colors = {
            'up': (80, 170, 255),    # Mavi
            'down': (255, 60, 90),    # Kırmızı
            'left': (60, 255, 160),   # Yeşil
            'right': (255, 240, 80),  # Sarı
        }
        push_color = dir_colors[self.direction]

        # Fill rengini neredeyse tamamen şeffaf yap
        rgba = to_rgba_float(push_color)
        rgba = (rgba[0], rgba[1], rgba[2], 0.1)  # Alpha ~1%

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        space.add(self.body)

        # Sensor circle - çarpışma olmadan algılar
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.sensor = True  # Çarpışma olmadan algıla
        self.shape.color = rgba
        self.shape.edge_color = to_rgba_float(push_color)
        self.shape.push_direction = self.direction
        self.shape.push_color = push_color
        self.shape.collision_type = 2  # Farklı collision type
        space.add(self.shape)

        self.radius = radius
        self.force_strength = force_strength
        self.center = pymunk.Vec2d(x, y)

        # Collision handlers: impulse on begin + small continuous force
        space.on_collision(1, 2, begin=self._on_begin, post_solve=self.apply_force)

    def apply_force(self, arbiter, space, data):
        """Topa zone içinde sürekli küçük kuvvet uygulama (post_solve)"""
        # Arbiter'de hangi şekil top ise onu bul
        if arbiter.shapes[0].collision_type == 1:
            ball_shape = arbiter.shapes[0]
        else:
            ball_shape = arbiter.shapes[1]
        ball_body = ball_shape.body

        dir = getattr(arbiter.shapes[0], 'push_direction', None) or getattr(arbiter.shapes[1], 'push_direction', None) or self.direction

        # Küçük sürekli kuvvet (daha az, sadece hafif etki)
        strength = self.force_strength * 0.08
        if dir == 'left':
            force = pymunk.Vec2d(-strength, 0)
        elif dir == 'right':
            force = pymunk.Vec2d(strength, 0)
        elif dir == 'up':
            force = pymunk.Vec2d(0, -strength)
        else:  # down
            force = pymunk.Vec2d(0, strength)

        ball_body.apply_force_at_world_point(force, ball_body.position)

    def _on_begin(self, arbiter, space, data):
        """Collision begin - anlık güçlü impulse uygula"""
        if arbiter.shapes[0].collision_type == 1:
            ball_shape = arbiter.shapes[0]
        else:
            ball_shape = arbiter.shapes[1]
        ball_body = ball_shape.body

        dir = getattr(arbiter.shapes[0], 'push_direction', None) or getattr(arbiter.shapes[1], 'push_direction', None) or self.direction

        imp = self.force_strength * 0.25
        if dir == 'left':
            impulse = pymunk.Vec2d(-imp, 0)
        elif dir == 'right':
            impulse = pymunk.Vec2d(imp, 0)
        elif dir == 'up':
            impulse = pymunk.Vec2d(0, -imp)
        else:
            impulse = pymunk.Vec2d(0, imp)

        # Topun kütlesine göre hafif ayar
        impulse = impulse * (ball_body.mass if hasattr(ball_body, 'mass') else 1)
        ball_body.apply_impulse_at_world_point(impulse, ball_body.position)
        return True

    def get_height(self):
        return self.radius * 2