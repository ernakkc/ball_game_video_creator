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
from obstacles.gravity_well import GravityWell
from obstacles.force_zone import ForceZone
from obstacles.spiral import Spiral
from obstacles.wave_slider import WaveSlider

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
        y = 400
        max_y = WORLD_HEIGHT - 1000  # Sonlara yaklaşınca engel ekleme

        OBSTACLES = [
            'bouncer', # düz top sektirici
            'conveyor', # hareketli bant
            'force_zone', # kuvvet bölgesi
            'funnel', # huni
            'gravity_well', # yerçekimi kuyusu
            'hammer', # çekiç
            'lucky_cup', # şanslı kupa
            'minefield', # mayın tarlası
            'plinko',   # plinko tahtası
            'seesaw',   # tahterevalli
            'spiral',   # spiral engel
            'wave_slider', # dalga kaydırıcı
            'windmill'  # yel değirmeni
        ]

        for _ in range(5):  # 1 set of obstacles
            random.seed(datetime.now().timestamp())
            random.shuffle(OBSTACLES)

            for obstacle_name in OBSTACLES:
                if y > max_y:
                    break
                obstacle = None
                if obstacle_name == 'plinko':
                    obstacle = Plinko(self.space, 0, y, 20, 9, color='plinko')
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'lucky_cup':
                    obstacle = LuckyCup(self.space, 0, y)
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'minefield':
                    obstacle = Minefield(self.space, 0, y)
                    self.obstacles.append(obstacle) 
                    y += obstacle.get_height()
                elif obstacle_name == 'seesaw':
                    obstacle = Seesaw(self.space, 0, y, w=400, h=20, angle=0, color='seesaw')
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'bouncer':
                    obstacle = Bouncer(self.space, 70, y, radius=50, color='bouncer')
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'funnel':
                    obstacle = Funnel(self.space, y)
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'conveyor':
                    y += 100
                    obstacles = [Conveyor(self.space, 150, y, direction=1), Conveyor(self.space, 450, y + 150, direction=-1), Conveyor(self.space, 150, y + 300, direction=1), Conveyor(self.space, 450, y + 450, direction=-1),]
                    for obs in obstacles:
                        self.obstacles.append(obs)
                    y += 800
                elif obstacle_name == 'windmill':
                    obstacles = [Windmill(self.space, SCREEN_WIDTH//2- 100, y), Windmill(self.space, SCREEN_WIDTH//2 + 100, y+200, rotation_speed=-3)] ; y += 500
                    for obs in obstacles:
                        self.obstacles.append(obs)
                elif obstacle_name == 'hammer':
                    obstacle = Hammer(self.space, 300, y)
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'gravity_well':
                    obstacles = [GravityWell(self.space, SCREEN_WIDTH//2-100, y), GravityWell(self.space, SCREEN_WIDTH//2+100, y)]
                    for obs in obstacles:
                        self.obstacles.append(obs)
                    y += 500
                elif obstacle_name == 'spiral':
                    obstacles = [Spiral(self.space, SCREEN_WIDTH//2 -150, y), Spiral(self.space, SCREEN_WIDTH//2 + 150, y), Spiral(self.space, SCREEN_WIDTH//2, y)]; y += 900
                    for obs in obstacles:
                        self.obstacles.append(obs)
                elif obstacle_name == 'wave_slider':
                    obstacle = WaveSlider(self.space, SCREEN_WIDTH//2, y)
                    self.obstacles.append(obstacle)
                    y += obstacle.get_height()
                elif obstacle_name == 'force_zone':
                    # Harita boyunca rastgele dağıt - 8-12 tane, çakışma kontrolü ile
                    num_zones = random.randint(8, 12)
                    for i in range(num_zones):
                        attempts = 0
                        while attempts < 25:
                            zx = random.randint(100, SCREEN_WIDTH - 100)
                            zy = random.randint(500, WORLD_HEIGHT - 500)  # Tüm harita boyunca

                            # Basit çakışma kontrolü: mevcut engellerin pozisyonlarına çok yakın olmasın
                            ok = True
                            for obs in self.obstacles:
                                if hasattr(obs, 'body') and obs.body is not None:
                                    ox, oy = obs.body.position
                                    if abs(ox - zx) < 120 and abs(oy - zy) < 120:
                                        ok = False
                                        break
                            if ok:
                                break
                            attempts += 1

                        zone = ForceZone(self.space, zx, zy, radius=80, force_strength=1800)
                        self.obstacles.append(zone)
                    y += 100  # Minimal artış

        self.wall_obstacles()