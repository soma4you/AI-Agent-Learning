import sqlite3
from pathlib import Path

DB_NAME = "test.db"

def get_db_connect(db_name: str|Path = DB_NAME)-> sqlite3.Connection:
    BASE_DIR = Path(__file__).parent
    DB_PATH = BASE_DIR / "data" / db_name
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row # 데이터 형태 변환(튜플 --> Dict)
    return conn