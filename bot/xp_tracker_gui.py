# tk_file.py
import tkinter as tk
from tkinter import ttk
from config import SharedConfig

class XpTrackerApp:
    def __init__(self, root, shared_config):
        self.root = root
        self.shared_config = shared_config
        self.root.title('XP Tracker GUI')

        self.label = ttk.Label(self.root, text='XP Tracker GUI')
        self.label.pack(padx=10, pady=10)

        self.xp_bar = ttk.Progressbar(self.root, orient='horizontal', length=200, mode='determinate')
        self.xp_bar.pack(pady=10)

        self.level_label = ttk.Label(self.root, text='Level: 1')
        self.level_label.pack(pady=10)

        self.update_gui(50, 1)  # Atualização da barra de progresso e rótulo de nível

    def update_gui(self, xp, level):
        self.xp_bar['value'] = xp
        self.level_label['text'] = f'Level: {level}'

        # Verifica se o usuário subiu de nível
        if xp >= self.shared_config.xp_to_next_level:
            self.shared_config.xp_to_next_level *= 1.2
            level += 1
            # Aumenta a quantidade de xp necessário para subir de nível
            
        # Atualiza o rótulo de nível com base no novo nível
        self.level_label['text'] = f'Level: {level}'

    def start_gui(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    shared_config = SharedConfig()
    app_instance = XpTrackerApp(root, shared_config)
    app_instance.start_gui()
