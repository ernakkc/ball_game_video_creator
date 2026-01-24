# Configuration settings for the game
import os

WIDTH, HEIGHT = 540, 960  # 9:16 aspect ratio
WORLD_HEIGHT = 42000 # Total height of the game world
FPS = 60  # Frames per second
GRAVITY = (0, 1300)  # Gravity vector
BALL_SIZE = 20  # Default ball size
BALL_MASS = 2  # Default ball mass - artırıldı
BALL_FRICTION = 0.6  # Friction coefficient for balls
MAX_BALL_SPEED = 2000  # Maximum ball speed to prevent tunneling
MAX_PARTICLES = 200  # Maximum number of particles on screen

GATE_TIME = 2.0  # Time a gate remains open (in frames)

SCREEN_WIDTH = WIDTH + 10  # Additional space for UI
SCREEN_HEIGHT = HEIGHT + 10  # Additional space for UI

OUTPUT_FRAMES_FOLDER = "output_frames"  # Folder for output frames
OUTPUT_FOLDER = "output"  # General output folder
SOUNDS_FOLDER = "assets/sounds"  # Folder for sound assets
PHOTOS_FOLDER = "assets/photos"  # Folder for photo assets

# Ensure output directories exist
os.makedirs(OUTPUT_FRAMES_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(SOUNDS_FOLDER, exist_ok=True)
os.makedirs(PHOTOS_FOLDER, exist_ok=True)

# Color definitions
NEON_WHITE      = (245, 245, 245)
NEON_BLACK      = (15, 15, 20)

NEON_RED        = (255, 60, 90)
NEON_GREEN      = (60, 255, 160)
NEON_BLUE       = (80, 170, 255)
NEON_YELLOW     = (255, 240, 80)
NEON_ORANGE     = (255, 140, 60)
NEON_PURPLE     = (190, 90, 255)
NEON_PINK       = (255, 110, 190)
NEON_CYAN       = (60, 255, 255)

NEON_LIME       = (170, 255, 60)
NEON_TEAL       = (60, 255, 210)
NEON_MAGENTA    = (255, 60, 255)

NEON_GRAY       = (140, 140, 160)
NEON_DARK_GRAY  = (35, 35, 50)

NEON_GOLD       = (255, 215, 90)
NEON_SILVER     = (210, 210, 230)
NEON_BRONZE     = (210, 140, 80)

COLORS = [
    NEON_RED, NEON_GREEN, NEON_BLUE, NEON_YELLOW,
    NEON_ORANGE, NEON_PURPLE, NEON_PINK, NEON_CYAN,
    NEON_LIME, NEON_TEAL, NEON_MAGENTA,
    NEON_GOLD, NEON_SILVER, NEON_BRONZE
]

BACKGROUND_COLOR = (22, 22, 30)   # Koyu neon arka plan
DEFAULT_OBSTACLE_COLOR = NEON_DARK_GRAY

# Background options for random selection
BACKGROUNDS = {
    "dark": {"name": "Uzay", "canvas": (15, 15, 30), "body": "linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%)"},
    "sunset": {"name": "Gün Batımı", "canvas": (26, 5, 5), "body": "linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)"},
    "ocean": {"name": "Okyanus", "canvas": (0, 16, 32), "body": "linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)"},
    "forest": {"name": "Orman", "canvas": (5, 21, 5), "body": "linear-gradient(135deg, #134e5e 0%, #71b280 100%)"},
    "neon": {"name": "Neon", "canvas": (16, 0, 21), "body": "linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%)"},
    "volcano": {"name": "Volkan", "canvas": (42, 5, 5), "body": "linear-gradient(135deg, #800000 0%, #ff4500 100%)"},
    "ice": {"name": "Buzul", "canvas": (5, 21, 37), "body": "linear-gradient(135deg, #e0f7fa 0%, #00bcd4 100%)"},
    "midnight": {"name": "Gece Yarısı", "canvas": (0, 0, 0), "body": "linear-gradient(135deg, #000000 0%, #434343 100%)"},
    "candy": {"name": "Şeker", "canvas": (42, 10, 26), "body": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"},
    "gold": {"name": "Altın", "canvas": (26, 21, 5), "body": "linear-gradient(135deg, #cac531 0%, #f3f9a7 100%)"}
}
BALL_COLOR = NEON_WHITE

# Obstacle settings
OBSTACLE_COLORS = {
    "wall": NEON_DARK_GRAY,        
    "platform": (255, 180, 60),    
    "lucky_cup": (180, 180, 200),  
    "plinko": (100, 200, 255),     
    "minefield": (255, 100, 120),  
    "seesaw": (120, 255, 180),     
    "bouncer": (220, 120, 255),    
    "funnel": (255, 150, 200),     
    "windmill": (100, 255, 255),   # Çift tanımlama kaldırıldı (Cyan seçildi)
    "slider": (255, 220, 100),     
    "hammer": (255, 120, 100),     
    "gravity_well": (200, 100, 255), 
}

OBSTACLE_COLORS_EDGE = {
    "wall": (50, 50, 60),           # ÖNERİ: Duvar sınırları biraz daha belli olsun diye açıldı
    "platform": (180, 126, 42),     # Gayet iyi
    "lucky_cup": (126, 126, 140),   # Gayet iyi
    "plinko": (70, 140, 180),       # Gayet iyi
    "minefield": (180, 70, 84),     # Gayet iyi
    "seesaw": (84, 180, 126),       # Gayet iyi
    "bouncer": (154, 84, 180),      # Gayet iyi
    "funnel": (180, 105, 140),      # Gayet iyi
    "windmill": (60, 160, 160),     # Ana renge göre ayarlandı
    "slider": (190, 140, 40),       # ÖNERİ: Çamurlu sarı yerine "Bal Rengi" kenar
    "hammer": (180, 84, 70),        # Gayet iyi
    "gravity_well": (140, 70, 180), # Gayet iyi
}
CAMERA_SMOOTH = 0.1  # Camera smoothing factor
CAMERA_START_Y = 100  # Initial camera Y position (tr: Başlangıç kamera Y konumu)
CAMERA_OFFSET_Y = 200  # Camera offset from the player (tr: Oyuncudan kamera ofseti. Oyuncunun biraz üstünde konumlandırmak için kullanılır.)
TRAIL_LENGTH = 10  # Length of the player's trail (performans için azaltıldı)


# OBSTACLE PHYSICS SETTINGS
OBSTACLE_DENSITY = 0.6  # Density of obstacles (tr: Engellerin yoğunluğu) 
OBSTACLE_FRICTION = 1.0  # Friction coefficient for obstacles (tr: Engellerin sürtünme katsayısı)
ELASTICITY = 0.6  # Elasticity for obstacle collisions (tr: Engellerin çarpışma esnekliği) - azaltıldı
DEFAULT_OBSTACLE_MASS = 20  # Default mass for dynamic obstacles (tr: Dinamik engeller için varsayılan kütle) - artırıldı
OBSTACLE_RADIUS = 15  # Default radius for circular obstacles (tr: Dairesel engeller için varsayılan yarıçap)
MAX_OBSTACLE_HEIGHT = 3000  # Maximum height for obstacles (tr: Engeller için maksimum yükseklik)

PLINKO_SPACING_X = 95  # Horizontal spacing between plinko pegs (tr: Plinko çivileri arasındaki yatay boşluk)
PLINKO_SPACING_Y = 100  # Vertical spacing between plinko rows (tr