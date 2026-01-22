# Ball Game Video Creator

ball-game-video-creator/
│
├── main.py                     # Programın girişi (loop burada)
│
├── config/
│   ├── settings.py             # Ekran, FPS, gravity, renkler
│   └── constants.py            # Sabit sayılar (collision type vs)
│
├── core/
│   ├── game.py                 # Game class (init, run, update)
│   ├── world.py                # Pymunk Space + gravity
│   ├── camera.py               # Kamera takibi / smoothing
│   ├── renderer.py             # Çizim işleri
│   └── event_manager.py        # Input & pygame eventleri
│
├── entities/
│   ├── __init__.py
│   ├── ball.py                 # Marble / top
│   └── base_entity.py          # Ortak entity sınıfı
│
├── obstacles/
│   ├── __init__.py
│   ├── base_obstacle.py        # Ortak obstacle sınıfı
│   ├── platform.py
│   ├── spinner.py
│   ├── peg.py
│   ├── gravity_well.py
│   └── moving_bar.py
│
├── levels/
│   ├── __init__.py
│   ├── level_base.py           # Level arayüzü
│   ├── level_01.py
│   ├── level_plinko.py
│   └── level_final.py
│
├── systems/
│   ├── collision.py            # Collision handler’lar
│   ├── physics.py              # Force, attract, helper
│   ├── culling.py              # Kamera dışı optimizasyon
│   └── recorder.py             # Video / frame export
│
├── utils/
│   ├── math_utils.py
│   ├── color_utils.py
│   └── timer.py
│
├── assets/
│   ├── sounds/
│   ├── fonts/
│   └── images/
│
└── requirements.txt

