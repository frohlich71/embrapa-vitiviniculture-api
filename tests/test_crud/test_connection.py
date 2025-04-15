from app.db.session import engine
from sqlmodel import text

def test_database_connection():
    """Test if we can connect to the database and query the processing table"""
    with engine.connect() as conn:
        # Test if we can execute a simple query
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        assert "processing" in tables, "Processing table not found in database"
        
        # Test if we can query the processing table
        result = conn.execute(text("SELECT * FROM processing LIMIT 1"))
        row = result.fetchone()
        print(f"First row from processing table: {row}")
        
        # Test table structure
        result = conn.execute(text("PRAGMA table_info(processing);"))
        columns = result.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"Column: {col}")