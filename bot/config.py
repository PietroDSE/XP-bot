#config.py
import sqlite3
class SharedConfig:
    def __init__(self):
        self.xp_to_next_level = 100
        self.allowed_channel_name = 'bot_active'
        self.message_count = {}
        self.user_levels = {}       
        self.user_xp = {}
        self.message_author = None

        self.db_connection = sqlite3.connect('xp_tracker.db')
        self.db_cursor = self.db_connection.cursor()
        #conecta ao banco de dados sqlite3

        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS messages
            (guild_id INTEGER, channel_id INTEGER, author_id INTEGER, content TEXT)''')
        self.db_connection.commit()
        #cria a tabela de dados caso a mesma não exista