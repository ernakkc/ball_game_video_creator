import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import OBSTACLE_COLORS, OBSTACLE_COLORS_EDGE, DEFAULT_OBSTACLE_COLOR, ELASTICITY, OBSTACLE_FRICTION, OBSTACLE_DENSITY, OBSTACLE_RADIUS, DEFAULT_OBSTACLE_MASS, PLINKO_SPACING_X, PLINKO_SPACING_Y, MAX_OBSTACLE_HEIGHT
from utils.color_utils import to_rgba_float

class Seesaw(BaseObstacle):
    def __init__(self, space, x, y, w=400, h=20, angle=0, color=DEFAULT_OBSTACLE_COLOR):
        super().__init__(space)

        # 4 tane seesaw oluştur: sol ve sağ yarıda çapraz konumda
        positions = [
            (190, y + 200),   # Sol üst
            (360, y + 400),   # Sağ orta
            (190, y + 600),   # Sol alt
            (360, y + 800),   # Sağ alt
        ]

        self.bodies = []
        self.shapes = []
        self.pivot_bodies = []
        self.pivot_joints = []

        for pos_x, pos_y in positions:
            # Dynamic body for physics interaction
            mass = 10
            moment = pymunk.moment_for_box(mass, (w, h))
            body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
            body.position = pos_x, pos_y
            body.angle = angle * (3.14159 / 180)  # Convert angle to radians

            # Pivot point for seesaw (center)
            pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            pivot_body.position = pos_x, pos_y
            pivot_joint = pymunk.PinJoint(pivot_body, body, (0, 0), (0, 0))
            space.add(pivot_joint)

            shape = pymunk.Poly.create_box(body, (300, h))
            shape.friction = OBSTACLE_FRICTION
            shape.elasticity = ELASTICITY

            # COLOR RESOLUTION 
            if color is None: resolved = OBSTACLE_COLORS.get('seesaw')
            elif isinstance(color, str): resolved = OBSTACLE_COLORS.get(color, OBSTACLE_COLORS.get('seesaw'))
            else: resolved = color
            shape.color = to_rgba_float(resolved)
            shape.edge_color = to_rgba_float(OBSTACLE_COLORS_EDGE.get('seesaw', resolved))
            
            space.add(body, shape)

            self.bodies.append(body)
            self.shapes.append(shape)
            self.pivot_bodies.append(pivot_body)
            self.pivot_joints.append(pivot_joint)

        # Ana body olarak ilkini ata (BaseObstacle için)
        self.body = self.bodies[0] if self.bodies else None
    
    def get_height(self):
        return 1000  # 4 seesaw ile toplam yükseklik