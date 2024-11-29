import sqlite3

def connect_db():
    conn = sqlite3.connect("news_data.db")
    return conn

def save_data(data, table_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    for item in data:
        # 수정된 부분: item["title"] 대신 item.title 사용
        cursor.execute(f"INSERT INTO {table_name} (title, content) VALUES (?, ?)", (item.title, item.content))

    conn.commit()
    conn.close()

def get_summary_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM summarized_news")
    rows = cursor.fetchall()
    conn.close()
    return rows
