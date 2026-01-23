from entities.base_entity import BaseEntity

class BaseObstacle(BaseEntity):
    def is_visible(self, camera_y, screen_h):
        y = self.body.position.y
        return camera_y - 400 < y < camera_y + screen_h + 400
