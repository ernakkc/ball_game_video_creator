from core.game import Game
from levels.level_random import LevelRandom

game = Game()
game.load_level(LevelRandom)
game.run()
