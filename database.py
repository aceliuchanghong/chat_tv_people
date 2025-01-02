import sqlite3
from sqlite3 import Error

DATABASE_FILE = "chat_tv.db"


def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)
    return conn


def create_tables(conn):
    """Create the necessary tables if they don't exist"""
    try:
        sql_create_characters_table = """ CREATE TABLE IF NOT EXISTS characters (
                                            id integer PRIMARY KEY,
                                            background text NOT NULL,
                                            created_at timestamp DEFAULT CURRENT_TIMESTAMP
                                        ); """

        sql_create_chat_history_table = """ CREATE TABLE IF NOT EXISTS chat_history (
                                            id integer PRIMARY KEY,
                                            character_id integer NOT NULL,
                                            message text NOT NULL,
                                            is_user integer NOT NULL,
                                            created_at timestamp DEFAULT CURRENT_TIMESTAMP,
                                            FOREIGN KEY (character_id) REFERENCES characters (id)
                                        ); """

        cursor = conn.cursor()
        cursor.execute(sql_create_characters_table)
        cursor.execute(sql_create_chat_history_table)
    except Error as e:
        print(e)


def initialize_database():
    """Initialize the database and create tables"""
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        conn.close()


def save_character_background(background):
    """Save a new character background to the database"""
    conn = create_connection()
    if conn is not None:
        try:
            sql = """ INSERT INTO characters(background)
                      VALUES(?) """
            cur = conn.cursor()
            cur.execute(sql, (background,))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)
        finally:
            conn.close()
    return None


def save_chat_message(character_id, message, is_user):
    """Save a chat message to the database"""
    conn = create_connection()
    if conn is not None:
        try:
            sql = """ INSERT INTO chat_history(character_id, message, is_user)
                      VALUES(?,?,?) """
            cur = conn.cursor()
            cur.execute(sql, (character_id, message, is_user))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)
        finally:
            conn.close()
    return None


def get_chat_history(character_id):
    """Retrieve chat history for a specific character"""
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM chat_history WHERE character_id=? ORDER BY created_at",
                (character_id,),
            )
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.close()
    return []
