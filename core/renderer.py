import pymunk.pygame_util

class Renderer:
    def __init__(self, screen, camera):
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.camera = camera

    def draw(self, space):
        self.draw_options.transform = pymunk.Transform.translation(
            0, -self.camera.y
        )
        space.debug_draw(self.draw_options)
