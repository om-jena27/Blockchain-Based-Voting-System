import sqlite3
from werkzeug.security import generate_password_hash
from blockchain import Block

DB_FILE = 'voting.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            has_voted BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    # Candidates table
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    # Blockchain table
    c.execute('''
        CREATE TABLE IF NOT EXISTS blockchain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_index INTEGER NOT NULL,
            timestamp REAL NOT NULL,
            voter_id_hash TEXT NOT NULL,
            candidate_id INTEGER NOT NULL,
            previous_hash TEXT NOT NULL,
            hash TEXT NOT NULL,
            eth_tx_hash TEXT DEFAULT 'N/A'
        )
    ''')
    
    # Run migration if needed
    try:
        c.execute("ALTER TABLE blockchain ADD COLUMN eth_tx_hash TEXT DEFAULT 'N/A'")
    except sqlite3.OperationalError:
        pass
    
    # Settings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    # Check if admin exists, if not create default admin
    c.execute("SELECT * FROM users WHERE is_admin = 1")
    if not c.fetchone():
        c.execute("INSERT INTO users (voter_id, password_hash, is_admin, has_voted) VALUES (?, ?, ?, ?)",
                  ('admin', generate_password_hash('admin123'), True, False))
        
    # Create genesis block if blockchain empty
    c.execute("SELECT * FROM blockchain")
    if not c.fetchone():
        from time import time
        c.execute("INSERT INTO blockchain (block_index, timestamp, voter_id_hash, candidate_id, previous_hash, hash, eth_tx_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (0, time(), "0", 0, "0", "0", "N/A"))
        
    conn.commit()
    conn.close()

def get_full_chain_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT block_index as 'index', timestamp, voter_id_hash, candidate_id, previous_hash, hash, eth_tx_hash FROM blockchain ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_latest_block():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT block_index as 'index', timestamp, voter_id_hash, candidate_id, previous_hash, hash, eth_tx_hash FROM blockchain ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        block = Block(
            row['index'], row['timestamp'], row['voter_id_hash'], row['candidate_id'], row['previous_hash'], row['eth_tx_hash']
        )
        block.hash = row['hash']
        return block
    return None

def add_block_to_db(block):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO blockchain (block_index, timestamp, voter_id_hash, candidate_id, previous_hash, hash, eth_tx_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (block.index, block.timestamp, block.voter_id_hash, block.candidate_id, block.previous_hash, block.hash, block.eth_tx_hash))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    return row['value'] if row else default

def set_setting(key, value):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?", (key, value, value))
    conn.commit()
    conn.close()
