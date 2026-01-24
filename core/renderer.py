import pygame
import pymunk
import pymunk.pygame_util
from random import randint, uniform
from config.settings import DEFAULT_OBSTACLE_COLOR, TRAIL_LENGTH, SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_HEIGHT
from utils.vec2px import vec2px


def create_gradient_surface(width, height, color1, color2):
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = color1[0] * (1 - ratio) + color2[0] * ratio
        g = color1[1] * (1 - ratio) + color2[1] * ratio
        b = color1[2] * (1 - ratio) + color2[2] * ratio
        pygame.draw.line(surface, (int(r), int(g), int(b)), (0, y), (width-1, y))
    return surface


class Renderer:
    def __init__(self, screen, camera, color1, color2):
        self.screen = screen
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.camera = camera
        self.color1 = color1
        self.color2 = color2
        self.gradient_surf = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, color1, color2)
        
        # Duvar gradyanları için önbellek
        self.vertical_wall_grad = create_gradient_surface(20, WORLD_HEIGHT, color1, color2)
        
        # Yıldızları başlat
        self.stars = []
        for i in range(150):
            self.stars.append({
                'x': randint(0, SCREEN_WIDTH),
                'y': randint(0, SCREEN_HEIGHT),
                'size': uniform(0, 2),
                'speed': uniform(0.2, 1.0)
            })

    def draw(self, space):
        self.screen.blit(self.gradient_surf, (0, 0))
        
        # Yıldızları çiz
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(star['x']), int(star['y'])), max(1, int(star['size'])))

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
                
                # Duvar kontrolü
                x_coords = [v[0] for v in verts]
                y_coords = [v[1] for v in verts]
                width = max(x_coords) - min(x_coords)
                height = max(y_coords) - min(y_coords)
                is_wall = (width < 50 or height < 50) and getattr(shape, "edge_color", None) is None
                
                if not is_wall:
                    pygame.draw.polygon(self.screen, color, verts)
                
                # Kenar çizgisi - duvarlar için hiç çizme
                edge_color = getattr(shape, "edge_color", None)
                if edge_color and not is_wall:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_color_rgb = (
                                int(edge_color[0] * 255),
                                int(edge_color[1] * 255),
                                int(edge_color[2] * 255),
                            )
                        else:
                            edge_color_rgb = tuple(int(c) for c in edge_color[:3])
                    else:
                        edge_color_rgb = DEFAULT_OBSTACLE_COLOR
                    pygame.draw.lines(self.screen, edge_color_rgb, True, verts, 3)
                
                # Duvarlar için sadece gradyan çiz (dikey olanlar için)
                if is_wall:
                    if width < height:  # Dikey duvar
                        # Önbellekten al
                        wall_surf = self.vertical_wall_grad.subsurface((0, 0, int(width), int(height)))
                        pos = (min(x_coords), min(y_coords))
                        self.screen.blit(wall_surf, pos)
                        
                        # Hafif iç kenar çizgisi
                        inner_x = max(x_coords) if min(x_coords) < SCREEN_WIDTH // 2 else min(x_coords)
                        pygame.draw.line(self.screen, (200, 200, 200), (inner_x, min(y_coords)), (inner_x, max(y_coords)), 1)
                    # Yatay duvarlar için gradyan yok, sadece hafif kenar
                    elif height < width:  # Yatay duvar
                        inner_y = max(y_coords) if min(y_coords) < WORLD_HEIGHT // 2 else min(y_coords)
                        pygame.draw.line(self.screen, (200, 200, 200), (min(x_coords), inner_y), (max(x_coords), inner_y), 1)

            elif isinstance(shape, pymunk.Circle):
                center = shape.body.local_to_world(shape.offset)
                pos = vec2px(self, center)
                pygame.draw.circle(self.screen, color, pos, int(shape.radius))
                
                # Kenar çizgisi
                edge_color = getattr(shape, "edge_color", None)
                if edge_color:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_color_rgb = (
                                int(edge_color[0] * 255),
                                int(edge_color[1] * 255),
                                int(edge_color[2] * 255),
                            )
                        else:
                            edge_color_rgb = tuple(int(c) for c in edge_color[:3])
                    else:
                        edge_color_rgb = DEFAULT_OBSTACLE_COLOR
                    pygame.draw.circle(self.screen, edge_color_rgb, pos, int(shape.radius), 3)

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
                
                # Kenar çizgisi
                edge_color = getattr(shape, "edge_color", None)
                if edge_color:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_color_rgb = (
                                int(edge_color[0] * 255),
                                int(edge_color[1] * 255),
                                int(edge_color[2] * 255),
                            )
                        else:
                            edge_color_rgb = tuple(int(c) for c in edge_color[:3])
                    else:
                        edge_color_rgb = DEFAULT_OBSTACLE_COLOR
                    pygame.draw.line(self.screen, edge_color_rgb, pa, pb, 4)
    
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



    def update_stars(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = randint(0, SCREEN_WIDTH)
