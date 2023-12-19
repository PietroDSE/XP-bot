# xp_tracker_gui.py
import tkinter as tk
from tkinter import ttk
from config import SharedConfig

class XpTrackerApp:
    def __init__(self, master, shared_config):
        self.message_author = None
        self.master = master
        self.shared_config = shared_config
        self.master.title('XP Tracker GUI')

        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.label = ttk.Label(self.master, text='XP Tracker GUI')
        self.label.pack(padx=10, pady=10)

        self.xp_bar = ttk.Progressbar(self.frame, mode='indeterminate')
        self.xp_bar.grid(row=3, column=0, columnspan=2, pady=10)

        self.level_label = ttk.Label(self.master, text='Level: 1')
        self.level_label.pack(pady=10)

        self.update_gui(200, 2)  # Atualização da barra de progresso e rótulo de nível
    
    
    def start_progress_bar(self):
        self.xp_bar.start()

    def stop_progress_bar(self):
        self.xp_bar.stop()

    def update_progress_bar(self, value):
        self.xp_bar['value'] = value

    def update_gui(self, xp, level):
        self.xp_bar['value'] = xp
        self.level_label['text'] = f'Level: {level}'

        # Verifica se o usuário subiu de nível
        if xp >= self.shared_config.xp_to_next_level and self.shared_config.message_author:
            self.shared_config.xp_to_next_level *= 1.2
            level += 1
            # Aumenta a quantidade de xp necessário para subir de nível

            # Exibe a mensagem de parabéns no console (você pode modificar isso conforme necessário)
            print(f"Boa {self.shared_config.message_author}! Você alcançou o Level {level}!")

        # Atualiza o rótulo de nível com base no novo nível
        self.level_label['text'] = f'Level: {level}'

    def start_gui(self):
        self.master.mainloop()

# config.py
class SharedConfig:
    def __init__(self):
        self.xp_to_next_level = 100
        self.allowed_channel_name = 'bot_active'
        self.message_count = {}
        self.message_author = None  # Adiciona essa linha para armazenar o autor da última mensagem
