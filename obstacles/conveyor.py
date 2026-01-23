import pymunk
from obstacles.base_obstacle import BaseObstacle
from config.settings import (
    OBSTACKLE_COLORS,
    DEFAULT_OBSTACLE_COLOR,
    ELASTICITY,
    OBSTACLE_FRICTION,
    MAX_OBSTACLE_HEIGHT,
)
from utils.color_utils import to_rgba_float


class Conveyor(BaseObstacle):
    """Konveyör bant - topları belirli yönde iter"""

    def __init__(
        self,
        space,
        x,
        y,
        width=300,
        height=20,
        velocity=6000,
        direction=1,
        color=DEFAULT_OBSTACLE_COLOR,
    ):
        super().__init__(space)

        if y > MAX_OBSTACLE_HEIGHT:
            return

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        space.add(self.body)

        # COLOR
        if color is None:
            resolved = OBSTACKLE_COLORS.get("slider")
        elif isinstance(color, str):
            resolved = OBSTACKLE_COLORS.get(color, OBSTACKLE_COLORS.get("slider"))
        else:
            resolved = color

        rgba = to_rgba_float(resolved)

        # PLATFORM
        self.platform = pymunk.Poly.create_box(self.body, (width, height))
        self.platform.friction = OBSTACLE_FRICTION
        self.platform.elasticity = ELASTICITY
        self.platform.color = rgba
        self.platform.surface_velocity = (velocity * direction, 0)
        space.add(self.platform)

        # ------------------
        # OKLAR (VISUAL ONLY)
        # ------------------
        self.arrows = []

        arrow_spacing = 80
        arrow_size = 14
        arrow_thickness = 2
        arrow_color = to_rgba_float((255, 255, 255))
        arrow_count = max(1, int(width / arrow_spacing))

        for i in range(arrow_count):
            offset_x = -width / 2 + (i + 0.5) * arrow_spacing

            if direction > 0:
                tip = (offset_x + arrow_size, 0)
                left = (offset_x, arrow_size / 2)
                right = (offset_x, -arrow_size / 2)
            else:
                tip = (offset_x - arrow_size, 0)
                left = (offset_x, arrow_size / 2)
                right = (offset_x, -arrow_size / 2)

            a1 = pymunk.Segment(self.body, tip, left, arrow_thickness)
            a2 = pymunk.Segment(self.body, tip, right, arrow_thickness)

            for a in (a1, a2):
                a.sensor = True
                a.color = arrow_color
                self.arrows.append(a)
                space.add(a)
