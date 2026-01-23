# Configuration settings for the game
import os

WIDTH, HEIGHT = 540, 960  # 9:16 aspect ratio
WORLD_HEIGHT = 42000 # Total height of the game world
FPS = 60  # Frames per second
GRAVITY = (0, 1300)  # Gravity vector
BALL_SIZE = 20  # Default ball size
BALL_MASS = 1  # Default ball mass
BALL_FRICTION = 0.6  # Friction coefficient for balls

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
BALL_COLOR = NEON_WHITE

# Obstacle settings
OBSTACKLE_COLORS = {
    "wall": NEON_DARK_GRAY,        # Duvar (geri planda kalır)
    "platform": NEON_ORANGE,       # Ana denge yüzeyi
    "lucky_cup": NEON_GRAY,        # Şans kupası
    "plinko": NEON_BLUE,           # Çivi alanı
    "minefield": NEON_RED,           # Mayın tarlası
    "seesaw": NEON_GREEN,          # Tahterevalli
    "bouncer": NEON_PURPLE,        # Trambolin
    "funnel": NEON_PINK,           # Huni
    "windmill": NEON_CYAN,         # Yel değirmeni
    "slider": NEON_YELLOW,         # Yatay kayıcı
    "hammer": NEON_RED,            # Çekiç
    "windmill": NEON_TEAL,         # Yel değirmeni
}


# Camera settings
CAMERA_SMOOTH = 0.1  # Camera smoothing factor
CAMERA_START_Y = 100  # Initial camera Y position (tr: Başlangıç kamera Y konumu)
CAMERA_OFFSET_Y = 200  # Camera offset from the player (tr: Oyuncudan kamera ofseti. Oyuncunun biraz üstünde konumlandırmak için kullanılır.)
TRAIL_LENGTH = 30  # Length of the player's trail (tr: Oyuncu izinin uzunluğu)


# OBSTACLE PHYSICS SETTINGS
OBSTACLE_DENSITY = 0.6  # Density of obstacles (tr: Engellerin yoğunluğu) 
OBSTACLE_FRICTION = 1.0  # Friction coefficient for obstacles (tr: Engellerin sürtünme katsayısı)
ELASTICITY = 0.6  # Elasticity for obstacle collisions (tr: Engellerin çarpışma esnekliği)
DEFAULT_OBSTACLE_MASS = 10  # Default mass for dynamic obstacles (tr: Dinamik engeller için varsayılan kütle)
OBSTACLE_RADIUS = 15  # Default radius for circular obstacles (tr: Dairesel engeller için varsayılan yarıçap)
MAX_OBSTACLE_HEIGHT = 3000  # Maximum height for obstacles (tr: Engeller için maksimum yükseklik)

PLINKO_SPACING_X = 95  # Horizontal spacing between plinko pegs (tr: Plinko çivileri arasındaki yatay boşluk)
PLINKO_SPACING_Y = 100  # Vertical spacing between plinko rows (tr