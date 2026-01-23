from core.game import Game
from levels.level_random import LevelRandom
import os
from datetime import datetime
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
from config.settings import FPS, OUTPUT_FRAMES_FOLDER, OUTPUT_FOLDER

game = Game()
game.record_video = True  # Video oluşturmak için True
game.load_level(LevelRandom)
results = game.run()

print("Oyun Sonuçları:")
for key, value in results.items():
    print(f"{key}: {value}")

frame_count = results['frame_count']
comments = results.get('comments', [])

print(f"\n{results['frame_count']} frame kaydedildi. Video oluşturuluyor...")  # Bilgi mesajı

# ==================== VİDEO OLUŞTURMA (MOVIEPY) ====================
# Tüm kaydedilen PNG dosyalarından video oluştur
clip = ImageSequenceClip([f"{OUTPUT_FRAMES_FOLDER}/frame_{i:05d}.png" for i in range(frame_count)], fps=FPS)  # 60 FPS'lik video

# ==================== SESLERİ VİDEOYA EKLE ====================
if comments:  # Eğer ses kayıtları varsa
    print(f"\n🎵 {len(comments)} ses kaydı kontrol ediliyor...")
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
                
                print(f"  ✓ {os.path.basename(sound_file)} @ {start_time:.1f}s → {start_time + max_duration:.1f}s (looped)")
            except Exception as e:
                print(f"  ⚠️ {os.path.basename(sound_file)} eklenemedi: {e}")
    
    # Eğer ses klipleri varsa videoya ekle
    if audio_clips:
        final_audio = CompositeAudioClip(audio_clips)  # Tüm sesleri birleştir
        clip = clip.set_audio(final_audio)  # Videoya sesi ekle
        print(f"\n✅ {len(audio_clips)} ses efekti videoya eklendi!")
    else:
        print("\n⚠️ Hiçbir ses eklenemedi")
else:
    print("\n⚠️ Kaydedilmiş ses yok")

print("\n🎥 Video dosyası oluşturuluyor...")
clip.write_videofile(f"{OUTPUT_FOLDER}/advanced_marble_race-{datetime.now().timestamp()}.mp4", codec="libx264", fps=FPS, audio=True, audio_codec='aac', preset='ultrafast', threads=8, verbose=False)  # Çok hızlı ayarlar

print("✅ Video hazır: advanced_marble_race.mp4")  # Başarı mesajı
