import math
import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACKLE_COLORS,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class Windmill(BaseObstacle):
    """Dönen yel değirmeni kanatları - topları farklı yönlere savurur"""
    
    def __init__(self, space, x, y, blade_count=4, blade_length=120, blade_width=15, 
                 rotation_speed=3, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)
        
        if y > MAX_OBSTACLE_HEIGHT:
            return
        
        # Merkez pivot (static)
        pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        pivot_body.position = x, y
        # add pivot to space so constraints can reference it
        space.add(pivot_body)

        # Dönen body (dynamic - motor ile döndürülecek)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        # give some inertia so it behaves nicely
        self.body.mass = 10
        self.body.moment = 10000

        # add rotating body to space before adding shapes
        space.add(self.body)

        # Motor joint - sabit dönüş hızı için
        motor = pymunk.SimpleMotor(pivot_body, self.body, rotation_speed)
        space.add(motor)

        # Pivot joint - pozisyonu sabitlemek için (one side STATIC, other DYNAMIC ok)
        pivot_joint = pymunk.PinJoint(pivot_body, self.body, (0, 0), (0, 0))
        space.add(pivot_joint)
        
        # Kanatları oluştur (dönen body'ye bağlı)
        self.blades = []
        angle_step = 2 * math.pi / blade_count
        
        rgba = to_rgba_float(OBSTACKLE_COLORS.get('windmill'))
        
        for i in range(blade_count):
            angle = i * angle_step
            # Kanat uç noktaları
            start = (0, 0)
            end = (blade_length * math.cos(angle), blade_length * math.sin(angle))

            blade = pymunk.Segment(
                self.body,
                start,
                end,
                blade_width
            )
            blade.friction = OBSTACLE_FRICTION
            blade.elasticity = ELASTICITY
            blade.color = rgba
            
            # Başlangıç açısı ayarla (angle is already in radians)
            self.body.angle = angle
            
            self.blades.append(blade)
            space.add(blade)
        
