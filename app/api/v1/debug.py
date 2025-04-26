import sqlite3
from fastapi import APIRouter

router = APIRouter()

@router.get("/tables")
def get_tables():
    conn = sqlite3.connect("/app/db/local.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return {"tables": cursor.fetchall()}