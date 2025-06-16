# inspect_both_dbs.py
import sqlite3
import pandas as pd
CREATE_SQL = '''
CREATE TABLE IF NOT EXISTS events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    type       TEXT,
    title      TEXT,
    deadline   INTEGER,
    duration   INTEGER,
    day        INTEGER,
    month      INTEGER,
    year       INTEGER,
    priority   INTEGER
)
'''
# your CREATE statement, once
def get_db_connection():
    conn = sqlite3.connect('flexibleevents.db')
    conn.row_factory = sqlite3.Row
    return conn
with get_db_connection() as con:
    con.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    title TEXT,
    deadline INTEGER,
    duration INTEGER,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    priority INTEGER
)
''')

def ensure_table(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_SQL)
    conn.commit()
    conn.close()

def insert_test_row(db_path='flexibleevents.db'):
    # make sure the table exists before inserting
    ensure_table(db_path)

    conn = sqlite3.connect(db_path)
    conn.execute('''
      INSERT INTO events(type, title, deadline, duration, day, month, year, priority)
      VALUES (?,?,?,?,?,?,?,?)
    ''', ('flexible','Test Event',781,2,15,6,2025,1))
    conn.commit()
    conn.close()
    print("Inserted a test row into", db_path)

def inspect_db(db_path):
    # also ensure the table exists before reading
    ensure_table(db_path)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM events", conn)
    except Exception as e:
        print(f"Error reading {db_path}: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    print(f"\n----- Contents of {db_path} -----")
    if df.empty:
        print("  (no rows)\n")
    else:
        print(df.to_string(index=False), "\n")
def remove_event(condition=None):
    try:
        con = get_db_connection()
        cur = con.cursor()

        if condition:
            query = f"DELETE FROM events WHERE {condition}"
        else:
            query = "DELETE FROM events"

        cur.execute(query)
        con.commit()
        print("Deletion successful.")
    except Exception as e:
        print(f"Error deleting data: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    insert_test_row()              # write one test row into flexibleevents.db
    inspect_db('events.db')# dump fixed‑events DB
    inspect_db('flexibleevents.db')# dump flexible‑events DB
    remove_event(id==5)
    
