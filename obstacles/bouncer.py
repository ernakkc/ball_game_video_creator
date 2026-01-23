import pymunk
from random import choice
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACKLE_COLORS,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class Bouncer(BaseObstacle):
    """Yüksek elasticity'li trambolinler - topları zıplatır"""
    
    def __init__(self, space, x, y, x_count=3, y_count=2, spacing=200, 
                 radius=25, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        
        # Renk çözümü
        if color is None:
            resolved = OBSTACKLE_COLORS.get('pinball')
        elif isinstance(color, str):
            resolved = OBSTACKLE_COLORS.get(color, OBSTACKLE_COLORS.get('pinball'))
        else:
            resolved = color
        
        rgba = to_rgba_float(resolved)
        
        self.bodies = []
        self.shapes = []
        
        for i in range(x_count):
            for j in range(y_count):
                bouncer_x = x + i * spacing
                bouncer_y = y + j * spacing
                
                if bouncer_x < 0 or bouncer_x > 2000 or bouncer_y > MAX_OBSTACLE_HEIGHT:
                    continue
                
                # Static body
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = bouncer_x, bouncer_y
                
                # Yüksek elasticity'li circle
                shape = pymunk.Circle(body, radius)
                shape.friction = OBSTACLE_FRICTION
                shape.elasticity = 2.0  # Çok yüksek - güçlü zıplama
                shape.color = rgba
                
                space.add(body, shape)
                self.bodies.append(body)
                self.shapes.append(shape)
        
        # Ana body reference
        self.body = self.bodies[0] if self.bodies else None
