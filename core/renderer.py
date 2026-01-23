import pygame
import pymunk
import pymunk.pygame_util
from config.settings import BACKGROUND_COLOR, DEFAULT_OBSTACLE_COLOR
from utils.vec2px import vec2px


class Renderer:
    def __init__(self, screen, camera):
        self.screen = screen
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.camera = camera

    def draw(self, space):
        self.screen.fill(BACKGROUND_COLOR)

        for shape in space.shapes:
            color = getattr(shape, "color", DEFAULT_OBSTACLE_COLOR)

            # RGBA float -> RGB int
            if isinstance(color, (tuple, list)) and len(color) >= 3:
                if max(color) <= 1.0:
                    color = (
                        int(color[0] * 255),
                        int(color[1] * 255),
                        int(color[2] * 255),
                    )
                else:
                    color = tuple(int(c) for c in color[:3])

            if isinstance(shape, pymunk.Poly):
                verts = [
                    vec2px(self, shape.body.local_to_world(v))
                    for v in shape.get_vertices()
                ]
                pygame.draw.polygon(self.screen, color, verts)

            elif isinstance(shape, pymunk.Circle):
                center = shape.body.local_to_world(shape.offset)
                pos = vec2px(self, center)
                pygame.draw.circle(self.screen, color, pos, int(shape.radius))

            elif isinstance(shape, pymunk.Segment):
                a = shape.body.local_to_world(shape.a)
                b = shape.body.local_to_world(shape.b)
                pa = vec2px(self, a)
                pb = vec2px(self, b)

                pygame.draw.line(
                    self.screen,
                    color,
                    pa,
                    pb,
                    max(1, int(shape.radius * 2))
                )


