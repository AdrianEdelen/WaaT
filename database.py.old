import sqlite3
import datetime

class sqlite_db:
    def __init__(self, db_file) -> None:
        self.db_file = db_file

    def initialize_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS story (
                id INTEGER PRIMARY KEY,
                word TEXT,
                timestamp DATETIME,
                user TEXT,
                createdOn DATETIME,
                meta_message TEXT,
                avatar_url
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_last_message (
                channel_id INTEGER PRIMARY KEY,
                message_id INTEGER
            )
        ''')
                    
        conn.commit()
        conn.close()

    def save_last_message(self, channel_id, message_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bot_last_message (channel_id, message_id)
            VALUES (?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET message_id = excluded.message_id;
        ''', (channel_id, message_id))
        conn.commit()
        conn.close()

    def get_last_bot_message(self, channel_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT message_id FROM bot_last_message WHERE channel_id = ?', (channel_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def insert_word(self, word, user, timestamp, meta_message, avatar_url):
        conn = sqlite3.connect(self.db_file)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO story (word, timestamp, user, createdOn, meta_message, avatar_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (word, timestamp, user, datetime.now(), meta_message, avatar_url))
            id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            print(f'entry already exists:{word} {timestamp} {user}')
            pass
        finally:
            conn.close()
            return id
    
    def get_message_by_id(self, id):
        """return a single message object"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM story WHERE id = ?', (id, ))
        message = cursor.fetchone()

        if message:
            print(f"Message Found {message}")
        else:
            print("Message not found with specified id")
        conn.close()
        return message
    
    def update_message_word(self, new_value, record_id):
        """Update the 'word' in the message column"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        sql = f'''UPDATE story
                SET word = ?
                WHERE id = ?'''
        
        cursor.execute(sql, (new_value, record_id))
        conn.commit()
        conn.close()

    def get_last_message(self):
        """Fetch all words from the database, ordered by their position in the story."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM story ORDER BY id DESC LIMIT 1')
        last_message = cursor.fetchone()
        conn.close()
        if last_message is None:
            return None  
        return last_message  

    def get_all_words(self):
        """Fetch all words from the database, ordered by their position in the story."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM story ORDER BY id ASC')
        words = cursor.fetchall()
        conn.close()
        return [word[0] for word in words]  # Assuming each row contains a single word in the first column.

    def get_all_words_detailed(self):
        """Fetch all words with details from the database, ordered by their position in the story."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        # Assuming 'user' contains the author name, and 'timestamp' is when the word was added
        cursor.execute('SELECT word, user, timestamp, meta_message, avatar_url  FROM story ORDER BY id ASC')
        words_detailed = cursor.fetchall()
        conn.close()
        # Create a list of dictionaries, each containing the word and its details
        words_with_details = [
            {"word": word, "author": user, "timestamp": timestamp, "meta_message": meta_message, "avatar_url": avatar_url}
            for word, user, timestamp, meta_message, avatar_url in words_detailed
        ]
        return words_with_details