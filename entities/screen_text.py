import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_HEIGHT

class ScreenText:
    """Ekranda modern, neon tarzı UI elementlerini yönetir (Görsele uygun)"""
    
    def __init__(self):
        # --- Modern ve Yuvarlak Font Ayarları ---
        # 'arial rounded mt bold', 'verdana' gibi fontlar bu stile daha uygun
        self.font_name = pygame.font.match_font('arial rounded mt bold', 'verdana', 'arial')
        
        self.font_large = pygame.font.Font(self.font_name, 28)   # Büyük başlıklar
        self.font_medium = pygame.font.Font(self.font_name, 18)  # Liste elemanları, ana metinler
        self.font_small = pygame.font.Font(self.font_name, 14)   # Alt başlıklar (LİDER, BÖLGE vb.)
        self.font_bold = pygame.font.Font(self.font_name, 16)
        self.font_bold.set_bold(True) # Sıralama başlığı için
        
        # --- Renk Paleti (Görüntüden alındı) ---
        self.color_white = (230, 230, 230)      # Genel beyaz metinler
        self.color_gray_text = (150, 150, 150)  # Alt başlıklar için gri
        
        self.color_cyan_title = (0, 220, 255)   # "ANLIK SIRALAMA" başlığı
        
        # Sıralama Renkleri
        self.color_rank1_gold = (255, 200, 50)  # #1 Altın sarısı
        self.color_rank2_blue = (80, 120, 255)  # #2 Neon mavi
        self.color_rank3_purple = (180, 80, 255)# #3 Neon mor
        self.color_rank4_red = (255, 60, 90)    # #4 Neon kırmızı
        self.color_leader_pink = (255, 50, 120) # Sol üstteki Lider ismi rengi
        self.color_zone_red = (255, 50, 80)     # Bölge ismi rengi

        # Arka Plan Renkleri (Yarı saydam)
        self.color_panel_bg = (20, 25, 35, 230)    # Ana panellerin koyu arka planı
        self.color_row_bg = (35, 40, 50, 200)      # Sıralama satırlarının arka planı
        self.color_row1_bg = (50, 45, 30, 220)     # 1. sıranın hafif altın sarısı arka planı

    def draw_rounded_panel(self, surface, rect, color, corner_radius=15):
        """Yardımcı Fonksiyon: Köşeleri yuvarlatılmış, yarı saydam bir panel çizer."""
        # Saydamlık destekleyen geçici bir yüzey oluştur
        panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        # Yuvarlatılmış dikdörtgeni bu yüzeye çiz
        pygame.draw.rect(panel_surface, color, panel_surface.get_rect(), border_radius=corner_radius)
        # Ana ekrana yapıştır
        surface.blit(panel_surface, rect.topleft)

    def draw_game_info(self, surface, balls, fps, elapsed_time, current_zone_name="NO ZONE"):
        """Üç paneli yan yana çizer: LEADER, ZONE, TIME."""
        leader = max(balls, key=lambda b: b.body.position.y) if balls else None
        
        # Panel Düzeni - Daha küçük
        panel_h = 38
        panel_w = 95
        margin_x = 15
        margin_y = 15
        gap = 8
        
        # --- 1. LİDER PANELİ ---
        lider_rect = pygame.Rect(margin_x, margin_y, panel_w, panel_h)
        self.draw_rounded_panel(surface, lider_rect, self.color_panel_bg, corner_radius=10)
        
        # Başlık: "LEADER"
        title_surf = self.font_small.render("LEADER", True, self.color_gray_text)
        title_rect = title_surf.get_rect(centerx=lider_rect.centerx, top=lider_rect.top + 3)
        surface.blit(title_surf, title_rect)
        
        # İsim: "Contestant X"
        leader_name = getattr(leader, 'name', '-') if leader else '-'
        name_color = self.color_leader_pink if leader else self.color_white
        name_surf = self.font_medium.render(leader_name, True, name_color)
        name_rect = name_surf.get_rect(centerx=lider_rect.centerx, bottom=lider_rect.bottom - 5)
        surface.blit(name_surf, name_rect)
        
        # --- 2. BÖLGE PANELİ ---
        bolge_rect = pygame.Rect(lider_rect.right + gap, margin_y, panel_w, panel_h)
        self.draw_rounded_panel(surface, bolge_rect, self.color_panel_bg, corner_radius=10)
        
        # Başlık: "ZONE"
        title_surf = self.font_small.render("ZONE", True, self.color_gray_text)
        title_rect = title_surf.get_rect(centerx=bolge_rect.centerx, top=bolge_rect.top + 3)
        surface.blit(title_surf, title_rect)
        
        # Bölge Adı
        zone_surf = self.font_medium.render(current_zone_name, True, self.color_zone_red)
        zone_rect = zone_surf.get_rect(centerx=bolge_rect.centerx, bottom=bolge_rect.bottom - 5)
        surface.blit(zone_surf, zone_rect)
        
        # --- 3. SÜRE PANELİ ---
        sure_rect = pygame.Rect(bolge_rect.right + gap, margin_y, panel_w, panel_h)
        self.draw_rounded_panel(surface, sure_rect, self.color_panel_bg, corner_radius=8)
        
        # Başlık: "TIME"
        title_surf = self.font_small.render("TIME", True, self.color_gray_text)
        title_rect = title_surf.get_rect(centerx=sure_rect.centerx, top=sure_rect.top + 3)
        surface.blit(title_surf, title_rect)
        
        # Süre
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        time_surf = self.font_medium.render(time_text, True, self.color_white)
        time_rect = time_surf.get_rect(centerx=sure_rect.centerx, bottom=sure_rect.bottom - 5)
        surface.blit(time_surf, time_rect)

    def draw_ball_stats(self, surface, balls, camera_y):
        """Sağ taraftaki 'LIVE RANKING' panelini çizer (Görsele birebir uygun)."""
        if not balls:
            return
        
        sorted_balls = sorted(balls, key=lambda b: b.body.position.y, reverse=True)
        
        # Ana Panel Boyut ve Konumu
        panel_w = 200
        num_racers = 4
        row_h = 28
        row_margin = 6
        panel_h = 45 + (row_h + row_margin) * num_racers
        
        panel_x = SCREEN_WIDTH - panel_w - 15
        panel_y = 15
        
        # 1. Ana Arka Plan Paneli
        main_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        self.draw_rounded_panel(surface, main_rect, self.color_panel_bg, corner_radius=20)
        
        # 2. Başlık: "LIVE RANKING"
        title_surf = self.font_bold.render("LIVE RANKING", True, self.color_cyan_title)
        surface.blit(title_surf, (panel_x + 15, panel_y + 12))
        
        # 3. Sıralama Satırları
        start_y = panel_y + 42
        
        for i, ball in enumerate(sorted_balls[:num_racers]):
            rank = i + 1
            name = getattr(ball, 'name', f'Contestant {rank}')
            # İlerleme yüzdesi
            progress = min(100, (ball.body.position.y / WORLD_HEIGHT) * 100)
            
            # Renk Seçimi (Görsele göre)
            if rank == 1:
                text_color = self.color_rank1_gold
                bg_color = self.color_row1_bg # 1. sıraya özel arka plan
            elif rank == 2:
                text_color = self.color_rank2_blue
                bg_color = self.color_row_bg
            elif rank == 3:
                text_color = self.color_rank3_purple
                bg_color = self.color_row_bg
            else: # rank 4 ve sonrası
                text_color = self.color_rank4_red
                bg_color = self.color_row_bg
            
            # Satır Arka Planı
            row_rect = pygame.Rect(panel_x + 10, start_y, panel_w - 20, row_h)
            self.draw_rounded_panel(surface, row_rect, bg_color, corner_radius=8)
            
            # İçerik Yerleşimi (Hizalama)
            padding_x = 12
            center_y = row_rect.centery
            
            # #X (Sıra No - Beyaz)
            rank_surf = self.font_medium.render(f"#{rank}", True, self.color_white)
            rank_rect = rank_surf.get_rect(left=row_rect.left + padding_x, centery=center_y)
            surface.blit(rank_surf, rank_rect)
            
            # İsim (Ortalı - Kendi renginde)
            name_surf = self.font_medium.render(name, True, text_color)
            name_rect = name_surf.get_rect(center=row_rect.center)
            surface.blit(name_surf, name_rect)
            
            # %XX (Yüzde - Beyaz)
            prog_surf = self.font_medium.render(f"%{int(progress)}", True, self.color_white)
            prog_rect = prog_surf.get_rect(right=row_rect.right - padding_x, centery=center_y)
            surface.blit(prog_surf, prog_rect)
            
            # Bir sonraki satır için Y koordinatını artır
            start_y += row_h + row_margin

    # --- Diğer Metodlar (Stile uygun sadeleştirildi) ---

    def draw_pause_overlay(self, surface):
        """Pause screen overlay"""
        darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        darken.fill((0, 0, 0, 180)) # Biraz daha koyu bir karartma
        surface.blit(darken, (0, 0))
        
        surf = self.font_large.render("GAME PAUSED", True, self.color_white)
        rect = surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(surf, rect)

    def draw_level_name(self, surface, level_name, duration=3.0, current_time=0):
        """Level ismi geçişi"""
        if current_time < duration:
            alpha = 255
            if current_time > duration - 1.0:
                alpha = int(255 * (duration - current_time))
            
            # Altın rengi, outline olmadan
            surf = self.font_large.render(f"- {level_name} -", True, self.color_rank1_gold)
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
            surface.blit(surf, rect)