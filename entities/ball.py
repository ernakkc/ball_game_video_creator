import pymunk
from entities.base_entity import BaseEntity
from config.settings import BALL_SIZE, BALL_MASS, BALL_FRICTION, BALL_COLOR, ELASTICITY, MAX_BALL_SPEED

class Ball(BaseEntity):
    def __init__(self, space, x, y):
        super().__init__(space)
        self.body = pymunk.Body(BALL_MASS, pymunk.moment_for_circle(BALL_MASS, 0, BALL_SIZE)) 
        self.body.position = x, y
        
        self.color = BALL_COLOR  # Default Beyaz renk
        self.name = "unnamed_ball" # Varsayılan isim
        self.photo = None  # Fotoğraf için yer tutucu
        self.sound = None  # Ses için yer tutucu
        self.body.mass = BALL_MASS
        self.size = BALL_SIZE
        self.trail = []  # İz listesi (trajectory)

        self.shape = pymunk.Circle(self.body, self.size) 
        self.shape.friction = BALL_FRICTION
        self.shape.color = BALL_COLOR
        self.shape.elasticity = ELASTICITY

        space.add(self.body, self.shape)
    
    def clamp_position(self, min_x, max_x, min_y, max_y):
        """Topun pozisyonunu sınırlar içinde tutar"""
        x, y = self.body.position
        clamped = False
        
        # X sınırları
        if x < min_x:
            x = min_x
            self.body.velocity = (abs(self.body.velocity.x) * 0.5, self.body.velocity.y)
            clamped = True
        elif x > max_x:
            x = max_x
            self.body.velocity = (-abs(self.body.velocity.x) * 0.5, self.body.velocity.y)
            clamped = True
        
        # Y sınırları
        if y < min_y:
            y = min_y
            self.body.velocity = (self.body.velocity.x, abs(self.body.velocity.y) * 0.5)
            clamped = True
        elif y > max_y:
            y = max_y
            self.body.velocity = (self.body.velocity.x, -abs(self.body.velocity.y) * 0.5)
            clamped = True
        
        if clamped:
            self.body.position = x, y
    
    def update(self, dt):
        """Topun hızını sınırla"""
        speed = self.body.velocity.length
        if speed > MAX_BALL_SPEED:
            self.body.velocity = (self.body.velocity / speed) * MAX_BALL_SPEED