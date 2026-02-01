import sys
import os
import subprocess

try:
    import pygame
except ImportError:
    print("Pygame not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame==2.6.1"])
    import pygame
try:    import pymunk
except ImportError:
    print("Pymunk not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymunk==7.2.0"])
    import pymunk
try:    import moviepy
except ImportError:
    print("MoviePy not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3"])
    import moviepy
try:    from PIL import Image
except ImportError:
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow==10.4.0"])
    from PIL import Image   


if __name__ == '__main__':
    if '--ui' in sys.argv:
        from ui.ball_setup_ui import BallSetupUI
        BallSetupUI().mainloop()
        sys.exit(0)
    else:
        # Import heavy modules only when running the game to avoid Tk/SDL conflicts on macOS
        from core.game import Game
        from levels.level_random import LevelRandom
        from datetime import datetime
        from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
        from config.settings import FPS, OUTPUT_FRAMES_FOLDER, OUTPUT_FOLDER

        game = Game()
        game.record_video = True
        game.load_level(LevelRandom)
        results = game.run()

        print("Game Results:")
        for key, value in results.items():
            try:
                print(f"{key}: {value}")
            except UnicodeEncodeError:
                # Handle Windows console encoding issues
                safe_value = str(value).encode('cp1252', errors='replace').decode('cp1252')
                print(f"{key}: {safe_value}")

        frame_count = results['frame_count']
        comments = results.get('comments', [])

        print(f"\n{results['frame_count']} frames recorded. Creating video...")  # Info message

        # ==================== VİDEO OLUŞTURMA (MOVIEPY) ====================
        # Tüm kaydedilen PNG dosyalarından video oluştur
        clip = ImageSequenceClip([f"{OUTPUT_FRAMES_FOLDER}/frame_{i:05d}.png" for i in range(frame_count)], fps=FPS)  # 60 FPS'lik video

        # ==================== SESLERİ VİDEOYA EKLE ====================
        if comments:  # Eğer ses kayıtları varsa
            print(f"\n{len(comments)} sound records checking...")
            audio_clips = []  # Tüm ses kliplerini tutacak liste

            for idx, item in enumerate(comments):  # Her ses kaydı için
                frame_num = item[0]  # Kare numarası
                comment_text = item[1]  # Yorum metni
                sound_file = item[2] if len(item) > 2 else None  # Ses dosyası (varsa)

                if sound_file and os.path.exists(sound_file):  # Eğer ses dosyası varsa
                    try:
                        start_time = frame_num / FPS  # Sesin başlama zamanı (saniye)

                        # Bir sonraki lider değişimi varsa, o zamana kadar çal
                        if idx + 1 < len(comments):
                            next_frame = comments[idx + 1][0]
                            end_time = next_frame / FPS
                            max_duration = end_time - start_time  # Ses bu kadar sürebilir
                        else:
                            max_duration = 5.0  # Son ses için maksimum 5 saniye

                        audio_clip_original = AudioFileClip(sound_file)  # Ses dosyasını yükle
                        original_duration = audio_clip_original.duration

                        # Sesi maksimum süreye göre döngü halinde tekrarla
                        if original_duration > 0 and max_duration > 0:
                            # Kaç kere tekrar etmesi gerektiğini hesapla
                            num_loops = int(max_duration / original_duration) + 1

                            # Her döngüyü ayrı ayrı ekle
                            for i in range(num_loops):
                                loop_start = start_time + (i * original_duration)
                                loop_clip = AudioFileClip(sound_file)

                                # Son döngü için kalan süreyi hesapla
                                remaining_time = (start_time + max_duration) - loop_start
                                if remaining_time <= 0:
                                    break

                                if remaining_time < original_duration:
                                    loop_clip = loop_clip.subclip(0, remaining_time)

                                loop_clip = loop_clip.set_start(loop_start)
                                loop_clip = loop_clip.volumex(0.5)
                                audio_clips.append(loop_clip)

                        print(f"  + {os.path.basename(sound_file)} @ {start_time:.1f}s → {start_time + max_duration:.1f}s (looped)")
                    except Exception as e:
                        safe_filename = os.path.basename(sound_file).encode('cp1252', errors='replace').decode('cp1252')
                        safe_error = str(e).encode('cp1252', errors='replace').decode('cp1252')
                        print(f"  Warning: {safe_filename} could not be added: {safe_error}")

            # Eğer ses klipleri varsa videoya ekle
            if audio_clips:
                final_audio = CompositeAudioClip(audio_clips)  # Tüm sesleri birleştir
                clip = clip.set_audio(final_audio)  # Videoya sesi ekle
                print(f"\n{len(audio_clips)} sound effects added to video!")
            else:
                print("\nNo sound added")
        else:
            print("\nNo recorded sound")

        print("\nCreating video file...")
        clip.write_videofile(f"{OUTPUT_FOLDER}/advanced_marble_race-{datetime.now().timestamp()}.mp4", codec="libx264", fps=FPS, audio=True, audio_codec='aac', preset='ultrafast', threads=8, verbose=False)  # Çok hızlı ayarlar

        print(f"Video ready: {OUTPUT_FOLDER}/advanced_marble_race.mp4")  # Başarı mesajı
