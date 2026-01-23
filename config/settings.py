# Configuration settings for the game
import os

WIDTH, HEIGHT = 540, 960  # 9:16 aspect ratio
WORLD_HEIGHT = 42000 # Total height of the game world
FPS = 60  # Frames per second
GRAVITY = (0, 1300)  # Gravity vector
BALL_SIZE = 10  # Default ball size
BALL_MASS = 1  # Default ball mass
BALL_FRICTION = 0.6  # Friction coefficient for balls

SCREEN_WIDTH = WIDTH + 50  # Additional space for UI
SCREEN_HEIGHT = HEIGHT + 50  # Additional space for UI

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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
TRANSPARENT = (0, 0, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
COLORS = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY, LIGHT_GRAY, DARK_GRAY, LIGHT_BLUE, DARK_GREEN, GOLD, SILVER, BRONZE, ORANGE, PURPLE, PINK, BROWN, CYAN, MAGENTA]

# Obstacle settings
OBSTACKLE_COLORS = {
    "wall": DARK_GRAY, # Duvar
    "platform": BROWN, # Platform (denge yüzeyi)
    "ramp": LIGHT_GRAY, # Rampa (eğimli yüzey)
    "plinko": BLUE, # Plinko (çivili engel)
    "pinball": RED, # Pinball (topun zıpladığı engel)
    "forest": GREEN, # Orman (ağaç engeli)
    "spinner": ORANGE, # Dönen engel (dönen disk)
    "hammer": PURPLE, # Çekiç (sallanarak engel oluşturan)
    "windmill": CYAN, # Yel değirmeni (dönen kanatlar)
    "slider": YELLOW, # Kaydırıcı (yatay hareket eden engel)
    "crusher": BLACK, # Ezici (dikey hareket eden engel)
    "gravity": MAGENTA, # Yerçekimi değiştirici (yerçekimini değiştiren engel)
    "sieve": GRAY, # Elek (topun içinden geçebileceği engel)
}

# Camera settings
CAMERA_SMOOTH = 0.1  # Camera smoothing factor
CAMERA_START_Y = 100  # Initial camera Y position (tr: Başlangıç kamera Y konumu)
CAMERA_OFFSET_Y = 200  # Camera offset from the player (tr: Oyuncudan kamera ofseti. Oyuncunun biraz üstünde konumlandırmak için kullanılır.)
TRAIL_LENGTH = 30  # Length of the player's trail (tr: Oyuncu izinin uzunluğu)


