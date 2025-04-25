import psycopg2
from psycopg2 import sql

config = {
    'host': 'localhost',
    'database': 'snake',
    'user': 'postgres',
    'password': '12345678'
}

def connect():
    return psycopg2.connect(**config)

def setup_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            level INTEGER NOT NULL,
            score FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_last_score(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT level, score FROM user_scores
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row if row else (0, 0)

def save_score(user_id, level, score):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_scores (user_id, level, score)
        VALUES (%s, %s, %s);
    """, (user_id, level, score))
    conn.commit()
    cur.close()
    conn.close()

def get_all_scores_for_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, level, score, created_at
        FROM user_scores
        WHERE user_id = %s
        ORDER BY created_at DESC;
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows