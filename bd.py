import sqlite3

DB_PATH = r'TG_bot_chenl\translate\translate_v2\db.db'

def init_db():
    """Создаёт таблицу пользователей, если она не существует"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                waiting_translate INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def set_user_flag(user_id: int, flag: bool):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (user_id, waiting_translate)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET waiting_translate = excluded.waiting_translate
        ''', (user_id, int(flag)))
        conn.commit()

def get_user_flag(user_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT waiting_translate FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        return bool(result[0]) if result else False
