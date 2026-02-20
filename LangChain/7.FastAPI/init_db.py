"""
FastAPI
    ㄴ 협업 시스템: 유지보수 -> 기능별로 파일을 분리
    1. db / 테이블 생성
    
"""

import sqlite3
from pathlib import Path

# -----------------------------------
# DB 경로 생성
# -----------------------------------
BASE_DIR = Path(__file__).parent
DB_NAME = "test.db"
DB_PATH = BASE_DIR / "data" / DB_NAME
DB_PATH.parent.mkdir(
    parents=True, # 전체 경로를 한 번에 생성
    exist_ok=True # 이미 존재하는 경우 무시
)

# -----------------------------------
# DB 연결
# -----------------------------------
conn = sqlite3.connect(str(DB_PATH))

# -----------------------------------
# SQL을 위한 "커서" 객체 생성
# -----------------------------------
cur = conn.cursor()
cur.execute("""
CREATE TABLE
IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

cur.execute("""
INSERT INTO users(name, email) VALUES
("홍길동", "hong@test.com"),
("김길동", "kim@test.com"),
("박길동", "park@test.com"),
("이길동", "lee@test.com")
""")

# 저장(테이블 반영)
conn.commit()

# 되돌리기
# conn.rollback()

cur.close()
conn.close()

print(f"DB Initialized!: {DB_PATH}")
