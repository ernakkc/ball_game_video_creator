import pygame
import pymunk
import math
import re
from random import randint, choice

from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, WORLD_HEIGHT, GATE_TIME, OUTPUT_FRAMES_FOLDER, BACKGROUNDS, MAX_PARTICLES
from config import settings
from config.user_settings import NAMES, PHOTOS, NUM_MARBLES, PHOTOS, COLORS, SOUNDS

from core.world import World
from core.camera import Camera
from core.renderer import Renderer
from core.event_manager import EventManager

from entities.ball import Ball
from entities.screen_text import ScreenText

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Random background seç
        selected_bg = choice(list(BACKGROUNDS.values()))
        settings.BACKGROUND_COLOR = selected_bg["canvas"]
        
        # Gradient renkleri çıkar
        match = re.search(r'linear-gradient\(.*?, (#\w+) \d+%, (#\w+) \d+%\)', selected_bg["body"])
        if match:
            color1_hex = match.group(1)
            color2_hex = match.group(2)
            def hex_to_rgb(hex_str):
                return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))
            color1 = hex_to_rgb(color1_hex)
            color2 = hex_to_rgb(color2_hex)
        else:
            color1 = selected_bg["canvas"]
            color2 = selected_bg["canvas"]
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        
        self.world = World(screen=self.screen)
        self.particles = []
        
        # Çarpışma efekti için handler - sadece top-engeller arası
        self.world.space.on_collision(1, 0, post_solve=self.on_ball_obstacle_collision)
        
        self.camera = Camera(SCREEN_HEIGHT)
        self.renderer = Renderer(self.screen, self.camera, color1, color2)
        self.events = EventManager()
        self.screen_text = ScreenText()

        # Create balls based on user settings
        self.balls = []
        
        # Rastgele ama çakışmayan pozisyonlar oluştur
        import random
        used_positions = []
        min_distance = 60  # Minimum mesafe toplar arası
        
        for i in range(NUM_MARBLES):
            attempts = 0
            max_attempts = 100
            
            while attempts < max_attempts:
                # Rastgele pozisyon
                x = random.randint(80, SCREEN_WIDTH - 80)
                y = random.randint(30, 150)
                
                # Diğer toplarla çakışma kontrolü
                valid = True
                for px, py in used_positions:
                    dist = math.hypot(x - px, y - py)
                    if dist < min_distance:
                        valid = False
                        break
                
                if valid:
                    used_positions.append((x, y))
                    break
                
                attempts += 1
            
            # Eğer uygun pozisyon bulunamadıysa güvenli fallback
            if attempts >= max_attempts:
                x = 100 + i * 50
                y = 50
            
            ball = Ball(self.world.space, x, y)
            ball.name = NAMES[i % len(NAMES)]
            ball.photo = PHOTOS[i % len(PHOTOS)]
            ball.color = COLORS[i % len(COLORS)]
            ball.sound = SOUNDS[i % len(SOUNDS)]
            ball.last_y = y  # Sıkışma tespiti için
            ball.stuck_count = 0  # Sıkışma sayacı
            self.balls.append(ball)

        self.level = None
        
        # Oyun zamanı ve istatistikler
        self.elapsed_time = 0.0
        self.paused = False
        self.level_start_time = 0.0
        
        # wait gate time
        self.gate_timer = GATE_TIME
        self.gate_opened = False  # Başlangıç itme için flag


    def load_level(self, level_cls):
        self.level = level_cls(self.world.space)
        self.level.build()
        self.level_start_time = 0.0
    
    def apply_gravity_wells(self):
        """Gravity well yakınındaki toplara çekim kuvveti uygula"""
        for shape in self.world.space.shapes:
            if hasattr(shape, 'collision_type') and shape.collision_type == 5:  # Gravity well
                well_pos = shape.body.position
                for ball in self.balls:
                    marble_body = ball.body
                    # NaN kontrol
                    if math.isnan(marble_body.position.x) or math.isnan(marble_body.position.y):
                        continue
                    
                    # Mesafe hesapla
                    dx = well_pos.x - marble_body.position.x
                    dy = well_pos.y - marble_body.position.y
                    dist = math.hypot(dx, dy)
                    
                    # Sadece 150px içindeyse çekim uygula
                    if dist < 150 and dist > 0:
                        force_magnitude = 3000 / (dist + 1)
                        marble_body.apply_force_at_world_point(
                            (dx * force_magnitude, dy * force_magnitude),
                            marble_body.position
                        )

    def run(self):
        self.running = True
        self.leader = None
        self.comments = [] # Lider değişimlerini kaydet
        self.frame_count = 0
        self.time_elipsed = 0.0
        
        # Lider sesi için özel kanal
        self.leader_sound_channel = pygame.mixer.Channel(1)  # Kanal 1'i lider sesi için ayır

        while self.running:
            # FPS sınırlaması - video için gerçek zamanlı kayıt
            self.clock.tick(FPS)
            dt = 1.0 / FPS  # Sabit zaman adımı
            self.running = self.events.process()
            
            # Klavye kontrolleri
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.paused = not self.paused
                pygame.time.wait(200)  # Debounce
            
            # Fizik güncelleme (pause değilse)
            if not self.paused:
                # Gate timer kontrolü - oyun başlangıcında bekle
                if self.gate_timer > 0:
                    self.gate_timer -= dt
                    # Timer sıfırlandığında hafif bir bekleme daha
                    if self.gate_timer <= 0:
                        self.gate_timer = 0
                        # Kapı açılınca rastgele yatay itme (yarış başladı!)
                        if not self.gate_opened:
                            import random
                            for ball in self.balls:
                                ball.body.apply_impulse_at_local_point(
                                    (random.uniform(-150, 150), random.uniform(50, 150)), 
                                    (0, 0)
                                )
                            self.gate_opened = True
                else:
                    # Normal fizik simülasyonu
                    self.world.space.step(dt)
                    
                    # Obstacle'ları güncelle (hareketli olanlar için)
                    for obstacle in self.level.obstacles:
                        if hasattr(obstacle, 'update'):
                            obstacle.update(dt)
                    
                    # Top hızlarını sınırla
                    for ball in self.balls:
                        ball.update(dt)
                    
                    # Particle'ları güncelle
                    self.particles = [p for p in self.particles if p.update(dt)]
                    
                    self.elapsed_time += dt
                    self.level_start_time += dt
                    self.time_elipsed += dt
                    
                    # Lider takibi
                    current_leader = max(self.balls, key=lambda b: b.body.position.y)
                    if self.leader != current_leader:
                        old_leader_name = self.leader.name if self.leader else "None"
                        new_leader_name = current_leader.name
                        
                        # Ses dosyasını kaydet (video için)
                        sound_file = current_leader.sound
                        
                        # Comments'e tuple olarak ekle (IFBL_python tarzı)
                        self.comments.append((self.frame_count, f"{new_leader_name} liderliği {old_leader_name}'den aldı!", sound_file))
                        
                        # Oyun sırasında sesi çal (sadece oynarken duyulsun) - DÖNGÜ İLE
                        try:
                            if self.leader_sound_channel.get_busy():
                                self.leader_sound_channel.stop()
                            sound = pygame.mixer.Sound(sound_file)
                            sound.set_volume(0.5)
                            self.leader_sound_channel.play(sound, loops=-1)  # Sonsuz döngü (-1)
                            print(f"🔊 Ses döngüde çalıyor: {new_leader_name}")
                        except Exception as e:
                            print(f"Ses çalma hatası: {e}")
                        self.leader = current_leader
                    
                    # Gravity well etkilerini uygula
                    self.apply_gravity_wells()
                    
                    # Sıkışma tespiti ve kurtarma (kapı açıldıktan 2 saniye sonra)
                    if self.frame_count > GATE_TIME * FPS + FPS * 2:
                        import random
                        for i, ball in enumerate(self.balls):
                            body = ball.body
                            
                            # NaN kontrolü
                            if math.isnan(body.position.x) or math.isnan(body.position.y):
                                body.position = (SCREEN_WIDTH / 2, 600)
                                body.velocity = (0, 0)
                                print(f"🔧 {ball.name} pozisyonu sıfırlandı (NaN)")
                                continue
                            
                            # Son Y pozisyonu kaydedildiyse
                            if hasattr(ball, 'last_y'):
                                # 5 pikselden az hareket ettiyse (sıkıştı!)
                                if abs(body.position.y - ball.last_y) < 5:
                                    ball.stuck_count += 1
                                    
                                    # 1.5 saniyeden fazla sıkışıksa
                                    if ball.stuck_count > FPS * 1.5:
                                        # Güçlü rastgele itme uygula (kurtar!)
                                        body.apply_impulse_at_local_point(
                                            (random.uniform(-200, 200), random.uniform(-300, -100)), 
                                            (0, 0)
                                        )
                                        ball.stuck_count = 0
                                        print(f"⚠️ {ball.name} sıkıştı, kurtarma itme uygulandı!")
                                    
                                    # 4 saniye hala sıkışıksa (kritik)
                                    if ball.stuck_count > FPS * 4:
                                        # Teleport: Liderin yanına gönder
                                        valid_positions = [b.body.position.y for b in self.balls 
                                                         if not math.isnan(b.body.position.y)]
                                        if valid_positions:
                                            leader_y = max(valid_positions)
                                            body.position = (
                                                SCREEN_WIDTH / 2 + random.uniform(-100, 100), 
                                                leader_y + 50
                                            )
                                            body.velocity = (0, 0)
                                            ball.stuck_count = 0
                                            print(f"🚀 {ball.name} teleport edildi!")
                                else:
                                    # Hareket ediyorsa sayacı sıfırla
                                    ball.stuck_count = 0
                                
                                ball.last_y = body.position.y
                    
                    # Topları sınırlar içinde tut
                    for ball in self.balls:
                        ball.clamp_position(
                            ball.size + 15,  # min_x (duvar kalınlığı + buffer)
                            SCREEN_WIDTH - ball.size - 15,  # max_x
                            10,  # min_y
                            WORLD_HEIGHT - 10  # max_y
                        )

            # ==================== FİNİŞ KONTROLÜ ====================
            finish_y = WORLD_HEIGHT - 100  # Finiş çizgisi
            marble_bodies = [ball.body for ball in self.balls]
            if any(body.position[1] >= finish_y for body in marble_bodies):  # Herhangi bir top finişe ulaştıysa
                print(f"\n🏁 YARIŞ BİTTİ! 🏁")  # Konsola yazdır
                winner_body = max(marble_bodies, key=lambda b: b.position[1])  # En uzakta olan topu bul (şampiyon)
                winner_ball = max(self.balls, key=lambda b: b.body.position[1])  # Şampiyon top objesi
                print(f"ŞAMPİYON: {winner_ball.name}")  # Şampiyon ismini yazdır
                print(f"SÜRE: {self.elapsed_time:.2f}s")  # Bitiş süresini yazdır
                
                # ==================== KUTLAMA EKRANI (3 SANİYE) ====================
                for extra in range(FPS * 3):  # 3 saniye = 180 kare
                    self.screen.fill((15, 15, 30))  # Ekranı temizle
                    # Şampiyon yazısı (çok büyük)
                    winner_text = pygame.font.SysFont("arial", 48, bold=True).render(f"ŞAMPİYON: {winner_ball.name}", True, winner_ball.color)
                    self.screen.blit(winner_text, (SCREEN_WIDTH / 2 - winner_text.get_width() / 2, SCREEN_HEIGHT / 2))  # Ekranın ortasına yaz
                    pygame.display.flip()  # Ekranı güncelle
                    # Kareyi kaydet (video modunda)
                    if self.record_video:
                        pygame.image.save(self.screen, f"output_frames/frame_{self.frame_count:05d}.png")
                        self.frame_count += 1  # Kare sayısını artır
                self.running = False  # Oyunu bitir
            
            leader_y = max(ball.body.position.y for ball in self.balls)
            self.camera.update(leader_y)
            
            # Performans optimizasyonu: kamera dışındaki engelleri pasif et
            self.world.update_obstacles_visibility(self.camera.y)

            # Render
            self.screen.fill((240, 240, 240))
            self.renderer.draw(self.world.space)
            
            # ==================== LİDER ÇEMBERİ ====================
            # Topları sırala (lideri belirlemek için)
            valid_positions = [(i, ball) for i, ball in enumerate(self.balls) if not math.isnan(ball.body.position.y)]
            sorted_positions = sorted(valid_positions, key=lambda item: item[1].body.position.y, reverse=True)
            
            # Lider için parlak çember çiz (toplardan önce) - Basitleştirilmiş
            if sorted_positions:
                leader_ball = sorted_positions[0][1]
                x, y = leader_ball.body.position
                screen_y = y - self.camera.y
                
                # Sadece ekranda görünüyorsa çiz
                if -50 < screen_y < SCREEN_HEIGHT + 50:
                    # Basit altın çember (alpha olmadan daha hızlı)
                    pygame.draw.circle(self.screen, (255, 215, 0), (int(x), int(screen_y)), leader_ball.size + 10, 3)
                    pygame.draw.circle(self.screen, (255, 240, 100), (int(x), int(screen_y)), leader_ball.size + 6, 2)
            
            # Topları izleriyle çiz
            self.renderer.draw_balls(self.balls)
            
            # Yıldızları güncelle
            self.renderer.update_stars()
            
            # Ekran yazılarını çiz
            fps = self.clock.get_fps()
            # Bölge belirleme
            if self.balls:
                leader = max(self.balls, key=lambda b: b.body.position.y)
                leader_y = leader.body.position.y
                if leader_y < WORLD_HEIGHT * 0.2:
                    zone_name = "Başlangıç"
                elif leader_y < WORLD_HEIGHT * 0.4:
                    zone_name = "İlk Bölge"
                elif leader_y < WORLD_HEIGHT * 0.6:
                    zone_name = "İkinci Bölge"
                elif leader_y < WORLD_HEIGHT * 0.8:
                    zone_name = "Üçüncü Bölge"
                elif leader_y < WORLD_HEIGHT * 0.9:
                    zone_name = "Dördüncü Bölge"
                else:
                    zone_name = "Final"
            else:
                zone_name = "Bölge Yok"
            self.screen_text.draw_game_info(self.screen, self.balls, fps, self.elapsed_time, zone_name)
            self.screen_text.draw_ball_stats(self.screen, self.balls, self.camera.y)
            
            # Gate countdown göster
            if self.gate_timer > 0:
                countdown_text = f"{int(self.gate_timer) + 1}"
                # Büyük font kullan ve animasyon ekle
                base_size = 150
                scale = 1 + 0.3 * math.sin(self.elapsed_time * 8)  # Nabız animasyonu
                font_size = int(base_size * scale)
                big_font = pygame.font.Font(None, font_size)
                countdown_surf = big_font.render(countdown_text, True, (255, 150, 50))  # Daha güzel turuncu-kırmızı
                countdown_rect = countdown_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                # Gölge
                shadow_surf = big_font.render(countdown_text, True, (100, 20, 0))  # Daha koyu gölge
                shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + int(6 * scale), SCREEN_HEIGHT // 2 + int(6 * scale)))
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(countdown_surf, countdown_rect)
            
            # Pause overlay
            if self.paused:
                self.screen_text.draw_pause_overlay(self.screen)
            
            # ==================== İSİMLER ====================
            font = pygame.font.SysFont("arial", 20, bold=True)  # Orta boy kalın yazı tipi
            
            # Her top için isim göster (ekranda görünüyorsa)
            for rank, (original_index, ball) in enumerate(sorted_positions[:10]):  # İlk 10 top
                x, y = ball.body.position
                screen_y = y - self.camera.y
                
                # Sadece ekranda görünüyorsa göster
                if -50 < screen_y < SCREEN_HEIGHT + 50:
                    # İsim metni
                    name_text = ball.name
                    
                    # Renk: Lider altın, diğerleri beyaz
                    text_color = self.screen_text.color_rank1_gold if rank == 0 else self.screen_text.color_white
                    
                    # Gölge ile çiz
                    text_surf = font.render(name_text, True, text_color)
                    shadow_surf = font.render(name_text, True, (0, 0, 0))
                    
                    # Topun üstünde konumlandır
                    text_x = int(x - text_surf.get_width() // 2)
                    text_y = int(screen_y - ball.size - 25)
                    
                    # Gölge çiz
                    self.screen.blit(shadow_surf, (text_x + 1, text_y + 1))
                    # Ana yazı çiz
                    self.screen.blit(text_surf, (text_x, text_y))
            
            pygame.display.flip()

            # Ekranı kaydet (sadece video kayıt modunda)
            if self.record_video:
                pygame.image.save(self.screen, f"{OUTPUT_FRAMES_FOLDER}/frame_{self.frame_count:05d}.png")
                self.frame_count += 1

        pygame.quit()
        # Oyun sonuçlarını döndür
        return {
            'frame_count': self.frame_count,
            'comments': self.comments,
            'elapsed_time': self.elapsed_time
        }
    
    def on_ball_obstacle_collision(self, arbiter, space, data):
        """Top engel çarpışmasında particle efekti"""
        from entities.particle import Particle
        import random
        
        # Sadece güçlü çarpışmalarda particle çıkar
        if arbiter.total_impulse.length < 10:  # Eşik değeri
            return True
        
        # Maksimum particle sayısını aşma
        if len(self.particles) >= MAX_PARTICLES:
            return True
        
        # Çarpışma noktası
        contact_point = arbiter.contact_point_set.points[0].point_a
        
        # 3-6 particle oluştur
        num_particles = random.randint(3, 6)
        for i in range(num_particles):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(200, 400)
            vx = speed * random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            vy = speed * random.uniform(-1, 1)
            
            particle = Particle(
                space, 
                contact_point.x, 
                contact_point.y, 
                vx, 
                vy, 
                lifetime=random.randint(20, 40),
                color=(255, 255, 255)
            )
            self.particles.append(particle)
        
        return True
