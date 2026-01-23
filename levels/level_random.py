from levels.level_base import BaseLevel
from obstacles.platform import Platform
from obstacles.spinner import Spinner

class LevelRandom(BaseLevel):
    def build(self):
        y = 200
        for i in range(6):
            self.obstacles.append(
                Platform(self.space, 450, y, 500, 20)
            )
            y += 250
            self.obstacles.append(
                Spinner(self.space, 450, y)
            )
            y += 250
