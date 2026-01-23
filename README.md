# Ball Game Video Creator

Bu proje, Pygame ve Pymunk kütüphanelerini kullanarak fizik tabanlı top oyunları simüle eden ve video çıkışı üreten bir Python uygulamasıdır. Kullanıcılar, çeşitli seviyeler ve engellerle top oyunları tasarlayabilir ve bunları video olarak kaydedebilir.

## Özellikler

- Fizik tabanlı simülasyon (Pymunk kullanarak)
- Birden fazla top desteği (isim, fotoğraf, renk, ses ile özelleştirilebilir)
- Çeşitli engeller: platformlar, spinner'lar, vb.
- Kamera takibi ve smoothing
- Video/frame çıkışı
- Rastgele ve özel seviyeler

## Kurulum

1. Gerekli bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Kullanıcı ayarlarını `config/user_settings.py` dosyasında yapılandırın:
   - Top sayısı (NUM_MARBLES)
   - İsimler (NAMES)
   - Fotoğraflar (assets/photos/ klasörüne ekleyin)
   - Renkler (otomatik olarak rastgele seçilir)

## Kullanım

1. Ana dosyayı çalıştırın:
   ```
   python main.py
   ```

2. Seviye yükleyin (örneğin, level_random):
   ```python
   game.load_level(LevelRandom)
   ```

3. Oyun döngüsü başlayacak ve video çerçeveleri `output_frames/` klasörüne kaydedilecek.

## Proje Yapısı

ball-game-video-creator/
│
├── main.py                     # Programın girişi (loop burada)
│
├── config/
│   ├── settings.py             # Ekran, FPS, gravity, renkler     
│   ├── user_settings.py        # Kullanıcı ayarları (isim, fotoğraf vs)
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

