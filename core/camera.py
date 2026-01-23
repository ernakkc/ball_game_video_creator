from config.settings import CAMERA_SMOOTH

class Camera:
    def __init__(self, height):
        self.y = 0
        self.height = height
        self.smooth = CAMERA_SMOOTH

    def update(self, target_y):
        desired = target_y - self.height // 3
        self.y += (desired - self.y) * self.smooth
        self.y = max(0, self.y)
