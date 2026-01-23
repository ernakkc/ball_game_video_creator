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


class Hammer(BaseObstacle):
    """Salınan çekiç - topları iterek yön değiştirir"""
    
    def __init__(self, space, x, y, arm_length=200, hammer_size=30, 
                 swing_angle=60, swing_speed=2, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        
        if y > MAX_OBSTACLE_HEIGHT:
            return
        
        # Pivot noktası (tavanda sabit)
        pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        pivot_body.position = x, y
        
        # Çekiç kolu ve başı (dynamic - fiziksel salınım)
        mass = 15
        moment = pymunk.moment_for_segment(mass, (0, 0), (0, arm_length), 5)
        self.body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y

        # add bodies to space before creating joints/shapes
        space.add(pivot_body, self.body)
        
        # Pivot joint (serbest salınım için)
        pivot_joint = pymunk.PinJoint(pivot_body, self.body, (0, 0), (0, 0))
        space.add(pivot_joint)
        
        # Rotary limit - salınım açısını sınırla
        angle_limit = math.radians(swing_angle)
        rotary_limit = pymunk.RotaryLimitJoint(
            pivot_body, self.body, -angle_limit, angle_limit
        )
        space.add(rotary_limit)
        
        # Renk çözümü
        if color is None:
            resolved = OBSTACKLE_COLORS.get('hammer')
        elif isinstance(color, str):
            resolved = OBSTACKLE_COLORS.get(color, OBSTACKLE_COLORS.get('hammer'))
        else:
            resolved = color
        
        rgba = to_rgba_float(resolved)
        
        # Çekiç kolu (segment)
        arm = pymunk.Segment(self.body, (0, 0), (0, arm_length), 5)
        arm.friction = OBSTACLE_FRICTION
        arm.elasticity = ELASTICITY
        arm.color = rgba
        space.add(arm)
        
        # Çekiç başı (circle)
        hammer_head = pymunk.Circle(self.body, hammer_size, (0, arm_length))
        hammer_head.friction = OBSTACLE_FRICTION
        hammer_head.elasticity = 1.5  # Yüksek elasticity - itiyor
        hammer_head.color = rgba
        space.add(hammer_head)
        
        # Başlangıç momentum (sallanmaya başlasın)
        self.body.angular_velocity = swing_speed
        
        self.shapes = [arm, hammer_head]
