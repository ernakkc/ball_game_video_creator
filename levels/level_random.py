from levels.level_base import BaseLevel
from obstacles.platform import Platform
from obstacles.plinko import Plinko
from obstacles.lucky_cup import LuckyCup
from obstacles.minefield import Minefield
from obstacles.seesaw import Seesaw
from obstacles.bouncer import Bouncer
from obstacles.funnel import Funnel
from obstacles.conveyor import Conveyor
from obstacles.windmill import Windmill
from obstacles.hammer import Hammer

from config.settings import SCREEN_WIDTH, WORLD_HEIGHT, OBSTACKLE_COLORS


class LevelRandom(BaseLevel):
    def wall_obstacles(self):
        w = 10
        h = WORLD_HEIGHT
        self.obstacles.append(Platform(self.space, w//2, h//2, w, h, color='wall'))
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH - w//2, h//2, w, h, color='wall'))
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH//2, 5, SCREEN_WIDTH, 10, color='wall'))
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH//2, WORLD_HEIGHT - 30, SCREEN_WIDTH, 60, color='wall'))

    def build(self):
        y = 400 # Starting Y position

        # self.obstacles.append(Plinko(self.space, 0, y, 20, 9, color='plinko')) # Parameters : 
        # y += 1000
        
        # self.obstacles.append(LuckyCup(self.space, 0, y))
        # y += 1000
        
        # self.obstacles.append(Minefield(self.space, 0, y))
        # y += 1000

        # self.obstacles.append(Seesaw(self.space, 0, y, w=400, h=20, angle=0, color='seesaw'))
        # y += 1000

        # self.obstacles.append(Bouncer(self.space, 70, y, radius=50, color='bouncer'))

        # self.obstacles.append(Funnel(self.space, y))

        # self.obstacles.append(Conveyor(self.space, 150, y))

        # self.obstacles.append(Windmill(self.space, 200, y))

        # self.obstacles.append(Hammer(self.space, 300, y))

        y += 1000
        for i in range(6):
            self.obstacles.append(
                Platform(self.space, 0, y, 500, 20, color='platform', angle=10)
            )
            y += 200


        self.wall_obstacles()