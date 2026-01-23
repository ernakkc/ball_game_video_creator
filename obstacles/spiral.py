import pymunk
import math
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACKLE_COLORS,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class Spiral(BaseObstacle):
    """Spiral ramp - toplar dönüş yaparak aşağı iner"""
    
    def __init__(self, space, x, y, radius=100, turns=2, segments=50, 
                 thickness=4, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        
        if y > MAX_OBSTACLE_HEIGHT:
            return
        
        # Static body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = 0, 0
        
        # Renk çözümü
        if color is None:
            resolved = OBSTACKLE_COLORS.get('ramp')
        elif isinstance(color, str):
            resolved = OBSTACKLE_COLORS.get(color, OBSTACKLE_COLORS.get('ramp'))
        else:
            resolved = color
        
        rgba = to_rgba_float(resolved)
        
        # Spiral noktaları oluştur
        points = []
        height_per_turn = 100
        total_height = turns * height_per_turn
        
        for i in range(segments + 1):
            t = i / segments
            angle = t * turns * 2 * math.pi
            
            # Spiral parametrik denklem
            px = x + math.cos(angle) * radius
            py = y + (t * total_height)
            points.append((px, py))
        
        # Segmentler oluştur
        self.segments = []
        for a, b in zip(points[:-1], points[1:]):
            seg = pymunk.Segment(self.body, a, b, thickness)
            seg.friction = OBSTACLE_FRICTION * 0.5  # Düşük sürtünme - kayarak inseler
            seg.elasticity = ELASTICITY
            seg.color = rgba
            self.segments.append(seg)
        
        space.add(self.body, *self.segments)
