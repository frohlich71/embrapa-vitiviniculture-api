from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS dummy_init (id INTEGER PRIMARY KEY)"))
    conn.commit()

print("✅ Banco garantido com escrita mínima.")