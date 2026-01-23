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

from config.settings import SCREEN_WIDTH, WORLD_HEIGHT, OBSTACLE_COLORS

from datetime import datetime
import random

class LevelRandom(BaseLevel):
    def wall_obstacles(self):
        w = 20  # Duvar kalınlığı
        h = WORLD_HEIGHT
        # Sol duvar
        self.obstacles.append(Platform(self.space, w//2, h//2, w, h, color='wall'))
        # Sağ duvar
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH - w//2, h//2, w, h, color='wall'))
        # Üst duvar
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH//2, 5, SCREEN_WIDTH, 20, color='wall'))
        # Alt duvar
        self.obstacles.append(Platform(self.space, SCREEN_WIDTH//2, WORLD_HEIGHT - 30, SCREEN_WIDTH, 60, color='wall'))

    def build(self):
        y = 400 # Starting Y position

        OBSTACLES = [
            'plinko',
            'lucky_cup',
            'minefield',
            'seesaw',
            'bouncer',
            'funnel',
            'conveyor',
            'windmill',
            'hammer',
        ]

        for _ in range(5):  # 5 sets of obstacles
            random.seed(datetime.now().timestamp())
            random.shuffle(OBSTACLES)

            for obstacle_name in OBSTACLES:
                obstacle = None
                if obstacle_name == 'plinko':
                    obstacle = Plinko(self.space, 0, y, 20, 9, color='plinko')
                elif obstacle_name == 'lucky_cup':
                    obstacle = LuckyCup(self.space, 0, y)
                elif obstacle_name == 'minefield':
                    obstacle = Minefield(self.space, 0, y)
                elif obstacle_name == 'seesaw':
                    obstacle = Seesaw(self.space, 0, y, w=400, h=20, angle=0, color='seesaw')
                elif obstacle_name == 'bouncer':
                    obstacle = Bouncer(self.space, 70, y, radius=50, color='bouncer')
                elif obstacle_name == 'funnel':
                    obstacle = Funnel(self.space, y)
                elif obstacle_name == 'conveyor':
                    obstacle = Conveyor(self.space, 150, y)
                elif obstacle_name == 'windmill':
                    obstacle = Windmill(self.space, 200, y)
                elif obstacle_name == 'hammer':
                    obstacle = Hammer(self.space, 300, y)
                
                if obstacle:
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height() + 100  # Ek spacing ile iç içe geçmeyi önle




        self.wall_obstacles()