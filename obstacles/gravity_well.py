import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACLE_COLORS,
    OBSTACLE_COLORS_EDGE,
    DEFAULT_OBSTACLE_COLOR,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class GravityWell(BaseObstacle):
    """Yerçekimi kuyusu - topları kendine çeker"""
    
    def __init__(self, space, x, y, radius=40, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        
        self.radius = radius
        
        if y > MAX_OBSTACLE_HEIGHT:
            return
        
        # Static body - hareketsiz çekim merkezi
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        space.add(self.body)
        
        # Renk çözümü
        if color is None:
            resolved = OBSTACLE_COLORS.get('gravity_well', (150, 50, 255))
        elif isinstance(color, str):
            resolved = OBSTACLE_COLORS.get(color, (150, 50, 255))
        else:
            resolved = color
        
        rgba = to_rgba_float(resolved)
        
        # Görsel çember (sensor - fiziksel çarpışma yok)
        visual_circle = pymunk.Circle(self.body, radius)
        visual_circle.sensor = True
        visual_circle.collision_type = 5  # Gravity well işareti
        visual_circle.color = rgba
        visual_circle.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('gravity_well', resolved))
        space.add(visual_circle)
        
        # İç çekirdek (görsel efekt için)
        core_circle = pymunk.Circle(self.body, radius // 3)
        core_circle.sensor = True
        core_circle.collision_type = 5
        core_circle.color = to_rgba_float((200, 100, 255, 1.0))
        core_circle.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('gravity_well', (200, 100, 255)))
        space.add(core_circle)
        
        self.shapes = [visual_circle, core_circle]
    
    def get_height(self):
        return self.radius * 2 + 100
