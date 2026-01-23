import pygame
import pymunk
import pymunk.pygame_util
from config.settings import BACKGROUND_COLOR, DEFAULT_OBSTACLE_COLOR, TRAIL_LENGTH, SCREEN_HEIGHT
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
    
    def draw_balls(self, balls):
        """İzli topları çizer (trajectory ile)"""
        for ball in balls:
            x, y = ball.body.position
            screen_y = y - self.camera.y
            
            # İz (trail) çiz
            if hasattr(ball, 'trail'):
                ball.trail.append((x, y))
                if len(ball.trail) > TRAIL_LENGTH:
                    ball.trail.pop(0)
                
                for j, (tx, ty) in enumerate(ball.trail):
                    trail_screen_y = ty - self.camera.y
                    progress = j / len(ball.trail)
                    trail_radius = int(ball.size * progress * 0.8)
                    
                    if trail_radius > 0 and -100 < trail_screen_y < SCREEN_HEIGHT + 100:
                        # Rengi soluğa dönür
                        faded_color = tuple(int(c * (0.3 + progress * 0.7)) for c in ball.color)
                        pygame.draw.circle(
                            self.screen, 
                            faded_color, 
                            (int(tx), int(trail_screen_y)), 
                            trail_radius
                        )
            
            # Topu çiz (izin üstüne)
            if -100 < screen_y < SCREEN_HEIGHT + 100:
                # Resim varsa çiz, yoksa renk
                if hasattr(ball, 'photo') and ball.photo and pygame.image.get_extended():
                    try:
                        # Resmi yükle ve boyutlandır
                        if not hasattr(ball, '_photo_surf'):
                            ball._photo_surf = pygame.image.load(ball.photo).convert_alpha()
                            ball._photo_surf = pygame.transform.scale(ball._photo_surf, (int(ball.size * 2), int(ball.size * 2)))
                            
                            # Çember şeklinde kırp
                            size = int(ball.size * 2)
                            circle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
                            pygame.draw.circle(circle_surf, (255, 255, 255, 255), (int(ball.size), int(ball.size)), int(ball.size))
                            ball._photo_surf = pygame.transform.scale(ball._photo_surf, (size, size))
                            ball._photo_surf.blit(circle_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                        
                        # Resmi çiz
                        photo_rect = ball._photo_surf.get_rect(center=(int(x), int(screen_y)))
                        self.screen.blit(ball._photo_surf, photo_rect)
                    except (pygame.error, FileNotFoundError):
                        # Resim yüklenemezse renk ile çiz
                        pygame.draw.circle(
                            self.screen, 
                            ball.color, 
                            (int(x), int(screen_y)), 
                            int(ball.size)
                        )
                else:
                    # Resim yoksa renk ile çiz
                    pygame.draw.circle(
                        self.screen, 
                        ball.color, 
                        (int(x), int(screen_y)), 
                        int(ball.size)
                    )


