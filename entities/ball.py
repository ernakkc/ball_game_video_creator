import pymunk
from entities.base_entity import BaseEntity
from config.settings import BALL_SIZE, BALL_MASS, BALL_FRICTION

class Ball(BaseEntity):
    def __init__(self, space, x, y):
        super().__init__(space)
        self.body = pymunk.Body(BALL_MASS, pymunk.moment_for_circle(BALL_MASS, 0, BALL_SIZE)) 
        self.body.position = x, y
        self.shape.friction = BALL_FRICTION
        self.color = (255, 255, 255)  # Default Beyaz renk
        self.name = "unnamed_ball" # Varsayılan isim
        self.photo = None  # Fotoğraf için yer tutucu
        self.sound = None  # Ses için yer tutucu
        self.body.mass = BALL_MASS
        self.size = BALL_SIZE
        self.shape = pymunk.Circle(self.body, self.size) 


        space.add(self.body, self.shape)
    
        