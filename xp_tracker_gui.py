import tkinter as tk
from tkinter import ttk

class XpTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('XP Tracker GUI')
        self.xp_to_next_level = 100  # Valor inicial de XP necessário para subir de nível

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

        # Verifica se o jogador subiu de nível
        if xp >= self.xp_to_next_level:
            self.xp_to_next_level *= 1.2 
            level += 1
        # Aumenta a quantidade de xp necessário para subir de nível
            
        # Atualiza o rótulo de nível com base no novo nível
        self.level_label['text'] = f'Level: {level}'

if __name__ == '__main__':
    root = tk.Tk()
    app = XpTrackerApp(root)
    root.mainloop()
