import pymunk
from obstacles.base_obstacle import BaseObstacle

class Spinner(BaseObstacle):
    def __init__(self, space, x, y):
        super().__init__(space)
        self.body = pymunk.Body(5, pymunk.moment_for_segment(5, (-60,0), (60,0), 5))
        self.body.position = x, y
        self.body.angular_velocity = 2
        self.shape = pymunk.Segment(self.body, (-60,0), (60,0), 6)
        space.add(self.body, self.shape)
