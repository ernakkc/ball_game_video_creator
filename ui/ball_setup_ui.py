import os
import threading
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

USER_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '../config/user_settings.py')
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), '../assets/photos')
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), '../assets/sounds')

class BallConfig:
    def __init__(self, name='', color='#ffffff', photo='', sound=''):
        self.name = name
        self.color = color
        self.photo = photo
        self.sound = sound

class BallSetupUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Ball Settings and Video Production')
        self.geometry('900x600')
        self.resizable(False, False)
        self.configure(bg='#232946')
        self.ball_count = tk.IntVar(value=4)
        self.video_count = tk.IntVar(value=1)
        self.ball_configs = []
        self.status_var = tk.StringVar(value='Ready')
        self.create_widgets()
        self.update_ball_list()
        
        # Ball count değişikliklerini izle (widget'lar oluşturulduktan sonra)
        self.ball_count.trace_add('write', lambda *args: self.update_ball_list())

        # Terminal benzeri çıktı paneli
        self.log_text = tk.Text(self, height=10, width=110, bg='#181c2f', fg='#eebbc3', font=('Consolas', 11), state='disabled')
        self.log_text.place(x=30, y=360, width=840, height=130)
        self.log_text.tag_config('info', foreground='#eebbc3')
        self.log_text.tag_config('warn', foreground='#ffb86c')
        self.log_text.tag_config('err', foreground='#ff5555')
        self.log_text.tag_config('ok', foreground='#50fa7b')

    def create_widgets(self):
        # Ball count selection
        tk.Label(self, text='Ball Count:', font=('Arial', 14, 'bold'), bg='#232946', fg='#eebbc3').place(x=30, y=30)
        tk.Spinbox(self, from_=2, to=12, textvariable=self.ball_count, width=5, font=('Arial', 14)).place(x=150, y=30)
        
        # Video count selection
        tk.Label(self, text='Video Count:', font=('Arial', 14, 'bold'), bg='#232946', fg='#eebbc3').place(x=250, y=30)
        tk.Spinbox(self, from_=1, to=10, textvariable=self.video_count, width=5, font=('Arial', 14)).place(x=370, y=30)
        
        # Ball list frame with scrollbar
        # Canvas ve scrollbar için konteyner
        self.scroll_container = tk.Frame(self, bg='#232946')
        self.scroll_container.place(x=30, y=80, width=840, height=270)
        
        # Canvas oluştur
        self.canvas = tk.Canvas(self.scroll_container, bg='#232946', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar oluştur
        self.scrollbar = tk.Scrollbar(self.scroll_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas'ı scrollbar'a bağla
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Canvas içine frame yerleştir
        self.ball_frame = tk.Frame(self.canvas, bg='#232946')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.ball_frame, anchor='nw')
        
        # Frame boyutu değiştiğinde canvas scroll bölgesini güncelle
        self.ball_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        # Canvas genişliği değiştiğinde frame genişliğini ayarla
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        # Mouse wheel ile scroll
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        
        # Başlat butonu
        self.start_btn = tk.Button(self, text='Start Video Production', font=('Arial', 16, 'bold'), bg='#eebbc3', fg='#232946', command=self.on_start)
        self.start_btn.place(x=320, y=500, width=260, height=50)
        
        # Durum etiketi
        self.status_label = tk.Label(self, textvariable=self.status_var, font=('Arial', 13), bg='#232946', fg='#eebbc3')
        self.status_label.place(x=30, y=560)
    
    def _on_mousewheel(self, event):
        """Mouse wheel ile scroll"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_ball_list(self):
        for widget in self.ball_frame.winfo_children():
            widget.destroy()
        count = self.ball_count.get()
        while len(self.ball_configs) < count:
            self.ball_configs.append(BallConfig())
        while len(self.ball_configs) > count:
            self.ball_configs.pop()
        for i in range(count):
            self.create_ball_row(i)
        # Frame yüksekliğini ayarla (her satır 60 piksel)
        total_height = count * 60
        self.ball_frame.config(height=total_height)
        # Canvas scroll bölgesini güncelle
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def create_ball_row(self, idx):
        y = idx * 60
        bc = self.ball_configs[idx]
        # İsim
        tk.Label(self.ball_frame, text=f'Ball {idx+1}', font=('Arial', 12, 'bold'), bg='#232946', fg='#eebbc3').place(x=0, y=y+10)
        name_entry = tk.Entry(self.ball_frame, font=('Arial', 12), width=12)
        name_entry.place(x=80, y=y+10)
        name_entry.insert(0, bc.name)
        name_entry.bind('<KeyRelease>', lambda e, i=idx: self.set_name(i, e.widget.get()))
        # Fotoğraf
        photo_btn = tk.Button(self.ball_frame, text='Choose Photo', command=lambda i=idx: self.choose_photo(i), bg='#eebbc3', fg='#232946')
        photo_btn.place(x=220, y=y+8, width=110)
        photo_label = tk.Label(self.ball_frame, text=os.path.basename(bc.photo) if bc.photo else 'None', bg='#232946', fg='#eebbc3', font=('Arial', 10))
        photo_label.place(x=340, y=y+12)
        # Renk
        color_btn = tk.Button(self.ball_frame, text='Choose Color', command=lambda i=idx: self.choose_color(i), bg=bc.color, fg='#232946')
        color_btn.place(x=440, y=y+8, width=90)
        # Ses
        sound_btn = tk.Button(self.ball_frame, text='Choose Sound', command=lambda i=idx: self.choose_sound(i), bg='#eebbc3', fg='#232946')
        sound_btn.place(x=540, y=y+8, width=110)
        sound_label = tk.Label(self.ball_frame, text=os.path.basename(bc.sound) if bc.sound else 'None', bg='#232946', fg='#eebbc3', font=('Arial', 10))
        sound_label.place(x=660, y=y+12)
        # Önizleme
        preview = tk.Canvas(self.ball_frame, width=30, height=30, bg='#232946', highlightthickness=0)
        preview.place(x=760, y=y+8)
        if bc.photo:
            try:
                img = Image.open(bc.photo)
                img = img.resize((30, 30))
                img = ImageTk.PhotoImage(img)
                preview.create_image(15, 15, image=img)
                preview.image = img
            except:
                preview.create_oval(2, 2, 28, 28, fill=bc.color, outline='')
        else:
            preview.create_oval(2, 2, 28, 28, fill=bc.color, outline='')

    def set_name(self, idx, name):
        self.ball_configs[idx].name = name

    def choose_photo(self, idx):
        file = filedialog.askopenfilename(initialdir=PHOTOS_DIR, title='Choose Photo', filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
        if file:
            self.ball_configs[idx].photo = file
            self.update_ball_list()

    def choose_color(self, idx):
        color = colorchooser.askcolor(title='Choose Color')[1]
        if color:
            self.ball_configs[idx].color = color
            self.update_ball_list()

    def choose_sound(self, idx):
        file = filedialog.askopenfilename(initialdir=SOUNDS_DIR, title='Choose Sound', filetypes=[('Sound Files', '*.wav *.mp3')])
        if file:
            self.ball_configs[idx].sound = file
            self.update_ball_list()

    def on_start(self):
        # Girişleri kontrol et
        for i, bc in enumerate(self.ball_configs):
            if not bc.name:
                messagebox.showerror('Missing Information', f'Please enter a name for Ball {i+1}!')
                return
            if not bc.photo and not bc.color:
                messagebox.showerror('Missing Information', f'Please choose a photo or color for Ball {i+1}!')
                return
            if not bc.sound:
                messagebox.showerror('Missing Information', f'Please choose a sound for Ball {i+1}!')
                return
        self.status_var.set('Video oluşturuluyor...')
        self.start_btn.config(state='disabled')
        threading.Thread(target=self.save_and_run, daemon=True).start()

    def save_and_run(self):
        try:
            import sys
            import subprocess
            self.save_user_settings()
            video_count = self.video_count.get()
            self.status_var.set(f'Creating {video_count} video(s)...')
            try:
                self.start_btn.config(state='disabled')
            except:
                pass

            # Terminal panelini temizle
            self.log_text.config(state='normal')
            self.log_text.delete('1.0', tk.END)
            self.log_text.config(state='disabled')

            for video_num in range(1, video_count + 1):
                if video_count > 1:
                    self.append_log(f'=== Creating Video {video_num}/{video_count} ===', tag='info')
                
                cmd = [sys.executable, os.path.join(os.path.dirname(__file__), '..', 'main.py')]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

                for line in proc.stdout:
                    line = line.rstrip()
                    if not line:
                        continue
                    self.append_log(line)
                    # Son satırı status olarak da göster
                    self.status_var.set(line[-120:])
                    self.log_text.see(tk.END)

                proc.wait()
                if proc.returncode == 0:
                    if video_count > 1:
                        self.append_log(f'Video {video_num} created successfully!', tag='ok')
                    else:
                        self.append_log('Video created!', tag='ok')
                else:
                    self.append_log(f'Error creating video {video_num}: process code {proc.returncode}', tag='err')
                    break  # Hata olursa sonraki videoları üretme

            if video_count > 1:
                self.append_log(f'All {video_count} videos completed!', tag='ok')
                self.status_var.set(f'All {video_count} videos created!')
            else:
                self.status_var.set('Video created!')
                
        except Exception as e:
            self.append_log(f'Error: {e}', tag='err')
            self.status_var.set(f'Error: {e}')
        finally:
            try:
                self.start_btn.config(state='normal')
            except:
                pass

    def append_log(self, text, tag=None):
        # Tag otomatik algılansın: [INFO], [WARN], [ERR], [OK]
        detected_tag = tag
        if text.startswith('[WARN]'):
            detected_tag = 'warn'
            text = text[6:].lstrip()
        elif text.startswith('[ERR]'):
            detected_tag = 'err'
            text = text[5:].lstrip()
        elif text.startswith('[OK]'):
            detected_tag = 'ok'
            text = text[4:].lstrip()
        elif text.startswith('[INFO]'):
            detected_tag = 'info'
            text = text[6:].lstrip()
        if not detected_tag:
            detected_tag = 'info'
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, text + '\n', detected_tag)
        self.log_text.config(state='disabled')

    def save_user_settings(self):
        # user_settings.py dosyasını güncelle
        lines = [
            'import os',
            'from config.settings import COLORS',
            'from random import sample',
            '',
            f'MAX_MARBLES = 12',
            f'MIN_MARBLES = 2',
            f'NUM_MARBLES = {len(self.ball_configs)}',
            '',
            'NAMES = [',
        ]
        for bc in self.ball_configs:
            lines.append(f'    "{bc.name}",')
        lines.append(']')
        # Renkler
        lines.append('COLORS = [')
        for bc in self.ball_configs:
            if bc.photo:
                lines.append('    (255,255,255),')
            else:
                rgb = self.hex_to_rgb(bc.color)
                lines.append(f'    ({rgb[0]},{rgb[1]},{rgb[2]}),')
        lines.append(']')
        # Fotoğraflar
        lines.append('PHOTOS = [')
        for bc in self.ball_configs:
            lines.append(f'    r"{bc.photo}",')
        lines.append(']')
        # Sesler
        lines.append('SOUNDS = [')
        for bc in self.ball_configs:
            lines.append(f'    r"{bc.sound}",')
        lines.append(']')
        with open(USER_SETTINGS_PATH, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == '__main__':
    app = BallSetupUI()
    app.mainloop()
