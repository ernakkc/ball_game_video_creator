import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class ScreenText:
    """Ekranda sürekli güncellenen yazıları yönetir"""
    
    def __init__(self):
        # Font ayarları
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Renkler
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.color_red = (255, 50, 50)
        self.color_green = (50, 255, 50)
        self.color_blue = (50, 150, 255)
        self.color_yellow = (255, 255, 50)
        
        # Text shadow için offset
        self.shadow_offset = 2
        
    def draw_text_with_shadow(self, surface, text, x, y, font, color, shadow_color=(0, 0, 0)):
        """Gölgeli yazı çizer"""
        # Gölge
        shadow_surf = font.render(str(text), True, shadow_color)
        surface.blit(shadow_surf, (x + self.shadow_offset, y + self.shadow_offset))
        
        # Asıl yazı
        text_surf = font.render(str(text), True, color)
        surface.blit(text_surf, (x, y))
        
    def draw_game_info(self, surface, balls, fps, elapsed_time):
        """Oyun bilgilerini ekrana çizer"""
        # FPS (sol üst)
        fps_text = f"FPS: {int(fps)}"
        self.draw_text_with_shadow(surface, fps_text, 10, 10, self.font_small, self.color_white)
        
        # Süre (sağ üst)
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"Süre: {minutes:02d}:{seconds:02d}"
        time_surf = self.font_small.render(time_text, True, self.color_white)
        self.draw_text_with_shadow(surface, time_text, SCREEN_WIDTH - 150, 10, 
                                   self.font_small, self.color_white)
        
        # Top sayısı
        ball_count = f"Toplar: {len(balls)}"
        self.draw_text_with_shadow(surface, ball_count, 10, 40, self.font_small, self.color_white)
        
        # Lider bilgisi (en önde olan top)
        if balls:
            leader = max(balls, key=lambda b: b.body.position.y)
            leader_text = f"Lider: {getattr(leader, 'name', 'Top')} - {int(leader.body.position.y)}m"
            self.draw_text_with_shadow(surface, leader_text, 10, 70, 
                                       self.font_medium, self.color_yellow)
        
    def draw_ball_stats(self, surface, balls, camera_y):
        """Her topun istatistiklerini ekrana çizer (sıralama tahtası)"""
        if not balls:
            return
        
        # Topları y pozisyonuna göre sırala (en önde olan en üstte)
        sorted_balls = sorted(balls, key=lambda b: b.body.position.y, reverse=True)
        
        # Sıralama tahtası başlığı
        title = "SIRALAMA"
        self.draw_text_with_shadow(surface, title, SCREEN_WIDTH - 250, 50, 
                                   self.font_medium, self.color_white)
        
        # Her top için bilgi
        y_offset = 90
        for i, ball in enumerate(sorted_balls[:10]):  # İlk 10 topu göster
            rank = i + 1
            name = getattr(ball, 'name', f'Top {i+1}')
            distance = int(ball.body.position.y)
            speed = int(ball.body.velocity.length)
            
            # Sıra numarası ve isim
            rank_color = self.color_yellow if rank == 1 else self.color_white
            rank_text = f"{rank}. {name}"
            self.draw_text_with_shadow(surface, rank_text, SCREEN_WIDTH - 240, y_offset, 
                                       self.font_small, rank_color)
            
            # Mesafe ve hız
            stats_text = f"{distance}m | {speed}px/s"
            self.draw_text_with_shadow(surface, stats_text, SCREEN_WIDTH - 240, y_offset + 20, 
                                       self.font_small, self.color_white)
            
            y_offset += 50
            
    def draw_instructions(self, surface):
        """Oyun talimatlarını gösterir"""
        instructions = [
            "ESC - Çıkış",
            "SPACE - Duraklat",
            "R - Yeniden Başlat"
        ]
        
        y_offset = SCREEN_HEIGHT - 100
        for instruction in instructions:
            self.draw_text_with_shadow(surface, instruction, 10, y_offset, 
                                       self.font_small, self.color_white)
            y_offset += 25
            
    def draw_pause_overlay(self, surface):
        """Oyun duraklatıldığında gösterilecek overlay"""
        # Yarı saydam siyah arka plan
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # DURAKLADI yazısı
        pause_text = "DURAKLADI"
        text_surf = self.font_large.render(pause_text, True, self.color_white)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(text_surf, text_rect)
        
    def draw_level_name(self, surface, level_name, duration=3.0, current_time=0):
        """Level adını belirli süre boyunca ekranda gösterir"""
        if current_time < duration:
            alpha = 255
            if current_time > duration - 1:  # Son 1 saniyede fade out
                alpha = int(255 * (duration - current_time))
            
            text = f"Level: {level_name}"
            text_surf = self.font_large.render(text, True, self.color_white)
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # Gölge
            shadow_surf = self.font_large.render(text, True, self.color_black)
            shadow_surf.set_alpha(alpha)
            shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 3, 103))
            surface.blit(shadow_surf, shadow_rect)
            
            # Asıl yazı
            surface.blit(text_surf, text_rect)
