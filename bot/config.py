#config.py
import sqlite3
class SharedConfig:
    xp_to_next_level = 100
    allowed_channel_name = 'bot_active'
    message_count = {}
    db_connection = sqlite3.connect('message.db')
    db_cursor = db_connection.cursor()