import os
from config.settings import COLORS
from random import sample

MAX_MARBLES = 12
MIN_MARBLES = 2
NUM_MARBLES = 4

NAMES = [
    "Turkey",
    "ABD",
    "Germany",
    "France"
    ]

# Randomly sample colors for marbles
COLORS = sample(COLORS, NUM_MARBLES)

# Load photos from assets/photos directory
PHOTOS = []
for file in os.listdir(os.path.join("assets", "photos")):
    if file.endswith(".png") or file.endswith(".jpg"):
        PHOTOS.append(os.path.join("assets", "photos", file))

# Load sounds from assets/sounds directory
SOUNDS = []
for file in os.listdir(os.path.join("assets", "sounds")):
    if file.endswith(".wav") or file.endswith(".mp3"):
        SOUNDS.append(os.path.join("assets", "sounds", file))
