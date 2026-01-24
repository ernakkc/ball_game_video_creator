import pygame
import pymunk
import pymunk.pygame_util
import math
from random import randint, uniform, choice
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
        
        # Arka plan ve Duvar Gradientleri
        self.gradient_surf = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, color1, color2)
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

        # --- BİTİŞ EKRANI (VICTORY SCREEN) DEĞİŞKENLERİ ---
        self.confetti = []
        self.animation_timer = 0
        self.ui_scale = 0
        # Fontları önceden yükle
        self.winner_font_large = pygame.font.SysFont("arial", 80, bold=True)
        self.winner_font_small = pygame.font.SysFont("arial", 24, bold=True)

    def update_stars(self):
        """Yıldızların kayma efekti"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = randint(0, SCREEN_WIDTH)

    def create_confetti(self):
        """Rengarenk konfetiler oluşturur"""
        colors = [(255, 60, 90), (80, 170, 255), (255, 240, 80), (60, 255, 160), (255, 255, 255)]
        return {
            'x': randint(0, SCREEN_WIDTH),
            'y': randint(-100, -10),
            'speed_y': uniform(2, 5),
            'speed_x': uniform(-1, 1),
            'color': choice(colors),
            'size': randint(4, 8),
            'angle': uniform(0, 360),
            'rotation_speed': uniform(-5, 5)
        }

    def draw_finish_line(self):
        """Bitiş çizgisi: kalın, renkli, parıltılı ve gölgeli"""
        y = WORLD_HEIGHT - 100
        line_width = SCREEN_WIDTH - 80
        x1 = 40
        x2 = x1 + line_width
        
        # Gölge
        pygame.draw.line(self.screen, (30, 30, 30), (x1, y+7 - self.camera.y), (x2, y+7 - self.camera.y), 12)
        # Ana çizgi (beyaz)
        pygame.draw.line(self.screen, (255, 255, 255), (x1, y - self.camera.y), (x2, y - self.camera.y), 8)
        
        # Renkli bloklar
        block_w = 32
        for i in range(line_width // block_w):
            color = [(255,60,90), (80,170,255), (255,240,80), (60,255,160)][i%4]
            pygame.draw.rect(self.screen, color, (x1 + i*block_w, y-12 - self.camera.y, block_w, 12))
        
        # Parıltı
        for i in range(3):
            alpha = 80 - i*25
            glow = pygame.Surface((line_width, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255,255,255,alpha), (0,0,line_width,24))
            self.screen.blit(glow, (x1, y-18 - self.camera.y))
            
        # "FINISH" yazısı
        font = pygame.font.SysFont("arial", 48, bold=True)
        text = font.render("FINISH", True, (255,255,255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y-40 - self.camera.y))
        self.screen.blit(text, text_rect)

    def draw_victory_screen(self, winner_ball):
        """Oyun bittiğinde çağrılacak modern kazanan ekranı"""
        self.animation_timer += 0.05
        
        # 1. Yarı saydam arka plan karartması
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 25, 200)) # Koyu lacivert tonlu saydamlık
        self.screen.blit(overlay, (0, 0))

        # 2. Konfeti Efekti
        if len(self.confetti) < 150:
            self.confetti.append(self.create_confetti())
        
        for p in self.confetti:
            p['y'] += p['speed_y']
            p['x'] += p['speed_x'] + math.sin(self.animation_timer + p['y']*0.01) * 0.5
            p['angle'] += p['rotation_speed']
            
            surf = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            pygame.draw.rect(surf, p['color'], (0, 0, p['size'], p['size']))
            rotated_surf = pygame.transform.rotate(surf, p['angle'])
            self.screen.blit(rotated_surf, (p['x'], p['y']))
            
            if p['y'] > SCREEN_HEIGHT:
                self.confetti.remove(p)

        # 3. Işık Hüzmesi (God Rays)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        rot_angle = self.animation_timer * 20
        ray_surf = pygame.Surface((800, 800), pygame.SRCALPHA)
        
        for i in range(0, 360, 20):
            rad = math.radians(i + rot_angle)
            end_x = 400 + math.cos(rad) * 400
            end_y = 400 + math.sin(rad) * 400
            pygame.draw.line(ray_surf, (255, 255, 255, 20), (400, 400), (end_x, end_y), 30)
        
        ray_rect = ray_surf.get_rect(center=(center_x, center_y))
        self.screen.blit(ray_surf, ray_rect)

        # 4. "ŞAMPİYON!" Başlığı
        # Hafif yukarı aşağı salınım
        float_y = math.sin(self.animation_timer * 2) * 10
        
        # Gölge
        shadow_text = self.winner_font_large.render("ŞAMPİYON!", True, (0, 0, 0))
        self.screen.blit(shadow_text, (center_x - shadow_text.get_width()//2 + 4, center_y - 180 + float_y + 4))
        
        # Asıl Yazı (Altın rengi)
        title_text = self.winner_font_large.render("ŞAMPİYON!", True, (255, 215, 0))
        self.screen.blit(title_text, (center_x - title_text.get_width()//2, center_y - 180 + float_y))

        # 5. Kazananın Avatarı/Topu
        ball_radius = 80
        ball_pos = (center_x, center_y + 20)
        
        # Arkasına parlama
        pygame.draw.circle(self.screen, (255, 255, 255, 40), ball_pos, ball_radius + 15 + math.sin(self.animation_timer*5)*5)
        
        if hasattr(winner_ball, 'photo') and winner_ball.photo:
            # Fotoğraf varsa
            if not hasattr(self, '_winner_surf'):
                try:
                    orig = pygame.image.load(winner_ball.photo).convert_alpha()
                    self._winner_surf = pygame.transform.smoothscale(orig, (ball_radius*2, ball_radius*2))
                    mask = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(mask, (255,255,255), (ball_radius, ball_radius), ball_radius)
                    self._winner_surf.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                except:
                    self._winner_surf = None

            if self._winner_surf:
                self.screen.blit(self._winner_surf, (ball_pos[0]-ball_radius, ball_pos[1]-ball_radius))
            else:
                pygame.draw.circle(self.screen, winner_ball.color, ball_pos, ball_radius)
        else:
            # Fotoğraf yoksa renkli top
            pygame.draw.circle(self.screen, winner_ball.color, ball_pos, ball_radius)
        
        # Topun etrafına altın çerçeve
        pygame.draw.circle(self.screen, (255, 215, 0), ball_pos, ball_radius, 6)

        # 6. Kazananın İsmi (Kutulu)
        name_text = winner_ball.name if hasattr(winner_ball, 'name') else "Yarışçı"
        name_surf = self.winner_font_small.render(name_text, True, (255, 255, 255))
        
        name_bg_rect = name_surf.get_rect(center=(center_x, center_y + 140))
        name_bg_rect.inflate_ip(60, 30)
        
        pygame.draw.rect(self.screen, (40, 40, 40), name_bg_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 215, 0), name_bg_rect, 2, border_radius=15)
        self.screen.blit(name_surf, name_surf.get_rect(center=name_bg_rect.center))


    def draw_balls(self, balls):
        """Topları ve izlerini çizer"""
        for ball in balls:
            x, y = ball.body.position
            screen_y = y - self.camera.y
            
            # İz (Trail) Çizimi
            if hasattr(ball, 'trail'):
                ball.trail.append((x, y))
                if len(ball.trail) > TRAIL_LENGTH:
                    ball.trail.pop(0)
                
                for j, (tx, ty) in enumerate(ball.trail):
                    trail_screen_y = ty - self.camera.y
                    progress = j / len(ball.trail)
                    trail_radius = int(ball.size * progress * 0.8)
                    
                    if trail_radius > 0 and -100 < trail_screen_y < SCREEN_HEIGHT + 100:
                        faded_color = tuple(int(c * (0.3 + progress * 0.7)) for c in ball.color)
                        pygame.draw.circle(
                            self.screen, 
                            faded_color, 
                            (int(tx), int(trail_screen_y)), 
                            trail_radius
                        )
            
            # Top Çizimi
            if -100 < screen_y < SCREEN_HEIGHT + 100:
                if hasattr(ball, 'photo') and ball.photo and pygame.image.get_extended():
                    try:
                        if not hasattr(ball, '_photo_surf'):
                            ball._photo_surf = pygame.image.load(ball.photo).convert_alpha()
                            ball._photo_surf = pygame.transform.scale(ball._photo_surf, (int(ball.size * 2), int(ball.size * 2)))
                            
                            size = int(ball.size * 2)
                            circle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
                            pygame.draw.circle(circle_surf, (255, 255, 255, 255), (int(ball.size), int(ball.size)), int(ball.size))
                            ball._photo_surf = pygame.transform.scale(ball._photo_surf, (size, size))
                            ball._photo_surf.blit(circle_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                        
                        photo_rect = ball._photo_surf.get_rect(center=(int(x), int(screen_y)))
                        self.screen.blit(ball._photo_surf, photo_rect)
                    except (pygame.error, FileNotFoundError):
                        pygame.draw.circle(self.screen, ball.color, (int(x), int(screen_y)), int(ball.size))
                else:
                    pygame.draw.circle(self.screen, ball.color, (int(x), int(screen_y)), int(ball.size))

    def draw(self, space):
        """Ana çizim fonksiyonu: Arka plan, engeller, bitiş çizgisi"""
        # 1. Arka Plan Gradient
        self.screen.blit(self.gradient_surf, (0, 0))
        
        # 2. Yıldızlar
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(star['x']), int(star['y'])), max(1, int(star['size'])))

        # 3. ForceZone'lar (Arka planda kalsın diye önce çiziliyor)
        for shape in list(space.shapes):
            if isinstance(shape, pymunk.Circle) and getattr(shape, 'collision_type', None) == 2:
                center = shape.body.local_to_world(shape.offset)
                pos = vec2px(self, center)
                pcol = getattr(shape, 'push_color', (200, 200, 200))
                surf_size = int(shape.radius * 2 + 12)
                temp_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
                c = (surf_size // 2, surf_size // 2)
                
                # ForceZone Görseli (Daha belirgin saydam daire + ok)
                circle_alpha = 110  # Daha görünür alpha
                pygame.draw.circle(temp_surf, (pcol[0], pcol[1], pcol[2], circle_alpha), c, int(shape.radius))
                pygame.draw.circle(temp_surf, (pcol[0], pcol[1], pcol[2], 200), c, int(shape.radius), 5)  # Kalın kenar
                arrow_length = shape.radius * 0.7
                arrow_alpha = 200  # Ok daha belirgin
                
                start, end, head = (0,0), (0,0), []
                direction = getattr(shape, 'push_direction', 'up')
                
                if direction == 'up':
                    start = (c[0], c[1] + int(arrow_length / 2))
                    end = (c[0], c[1] - int(arrow_length))
                    head = [(end[0] - 6, end[1] + 10), (end[0] + 6, end[1] + 10), end]
                elif direction == 'down':
                    start = (c[0], c[1] - int(arrow_length / 2))
                    end = (c[0], c[1] + int(arrow_length))
                    head = [(end[0] - 6, end[1] - 10), (end[0] + 6, end[1] - 10), end]
                elif direction == 'left':
                    start = (c[0] + int(arrow_length / 2), c[1])
                    end = (c[0] - int(arrow_length), c[1])
                    head = [(end[0] + 10, end[1] - 6), (end[0] + 10, end[1] + 6), end]
                else: # right
                    start = (c[0] - int(arrow_length / 2), c[1])
                    end = (c[0] + int(arrow_length), c[1])
                    head = [(end[0] - 10, end[1] - 6), (end[0] - 10, end[1] + 6), end]
                    
                pygame.draw.line(temp_surf, (pcol[0], pcol[1], pcol[2], arrow_alpha), start, end, 3)
                pygame.draw.polygon(temp_surf, (pcol[0], pcol[1], pcol[2], arrow_alpha), head)
                self.screen.blit(temp_surf, (pos[0] - surf_size // 2, pos[1] - surf_size // 2))

        # 4. Bitiş Çizgisi
        self.draw_finish_line()

        # 5. Fizik Objeleri (Engeller, Duvarlar)
        for shape in list(space.shapes):
            color = DEFAULT_OBSTACLE_COLOR
            if hasattr(shape, 'color'):
                color = shape.color
            
            # Renk dönüşümü (Float -> Int 0-255)
            if isinstance(color, (tuple, list)) and len(color) >= 3:
                if max(color) <= 1.0:
                    color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
                else:
                    color = tuple(int(c) for c in color[:3])

            # Polygon Çizimi
            if isinstance(shape, pymunk.Poly):
                verts = [vec2px(self, shape.body.local_to_world(v)) for v in shape.get_vertices()]
                
                # Duvar kontrolü
                x_coords = [v[0] for v in verts]
                y_coords = [v[1] for v in verts]
                width = max(x_coords) - min(x_coords)
                height = max(y_coords) - min(y_coords)
                is_wall = (width < 50 or height < 50) and getattr(shape, "edge_color", None) is None
                
                if not is_wall:
                    pygame.draw.polygon(self.screen, color, verts)
                
                # Kenar Çizgisi (Duvarlar hariç)
                edge_color = getattr(shape, "edge_color", None)
                if edge_color and not is_wall:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_rgb = (int(edge_color[0] * 255), int(edge_color[1] * 255), int(edge_color[2] * 255))
                        else:
                            edge_rgb = tuple(int(c) for c in edge_color[:3])
                        pygame.draw.lines(self.screen, edge_rgb, True, verts, 3)
                
                # Duvar Gradient İşlemleri
                if is_wall:
                    if width < height:  # Dikey Duvar
                        wall_surf = self.vertical_wall_grad.subsurface((0, 0, min(int(width), 20), min(int(height), WORLD_HEIGHT)))
                        pos = (min(x_coords), min(y_coords))
                        self.screen.blit(wall_surf, pos)
                        # İç ince çizgi
                        inner_x = max(x_coords) if min(x_coords) < SCREEN_WIDTH // 2 else min(x_coords)
                        pygame.draw.line(self.screen, (200, 200, 200), (inner_x, min(y_coords)), (inner_x, max(y_coords)), 1)
                    elif height < width:  # Yatay Duvar
                        inner_y = max(y_coords) if min(y_coords) < WORLD_HEIGHT // 2 else min(y_coords)
                        pygame.draw.line(self.screen, (200, 200, 200), (min(x_coords), inner_y), (max(x_coords), inner_y), 1)

            # Daire Çizimi
            elif isinstance(shape, pymunk.Circle):
                if getattr(shape, 'collision_type', None) == 2: continue # ForceZone'ları atla
                
                center = shape.body.local_to_world(shape.offset)
                pos = vec2px(self, center)
                pygame.draw.circle(self.screen, color, pos, int(shape.radius))
                
                edge_color = getattr(shape, "edge_color", None)
                if edge_color:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_rgb = (int(edge_color[0] * 255), int(edge_color[1] * 255), int(edge_color[2] * 255))
                        else:
                            edge_rgb = tuple(int(c) for c in edge_color[:3])
                        pygame.draw.circle(self.screen, edge_rgb, pos, int(shape.radius), 3)

            # Segment (Çizgi) Çizimi
            elif isinstance(shape, pymunk.Segment):
                a = shape.body.local_to_world(shape.a)
                b = shape.body.local_to_world(shape.b)
                pa = vec2px(self, a)
                pb = vec2px(self, b)
                
                pygame.draw.line(self.screen, color, pa, pb, max(1, int(shape.radius * 2)))
                
                edge_color = getattr(shape, "edge_color", None)
                if edge_color:
                    if isinstance(edge_color, (tuple, list)) and len(edge_color) >= 3:
                        if max(edge_color) <= 1.0:
                            edge_rgb = (int(edge_color[0] * 255), int(edge_color[1] * 255), int(edge_color[2] * 255))
                        else:
                            edge_rgb = tuple(int(c) for c in edge_color[:3])
                        pygame.draw.line(self.screen, edge_rgb, pa, pb, 4)