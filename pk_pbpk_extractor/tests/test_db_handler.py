import os
import sqlite3
from pk_pbpk_extractor.storage.db_handler import setup_database, get_connection

def test_db_setup(monkeypatch):
    test_db = "test_db.sqlite"
    monkeypatch.setenv("DB_PATH", f"sqlite:///{test_db}")
    
    setup_database()
    
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert "documents" in tables
    assert "pk_parameters" in tables
    
    conn.close()
    if os.path.exists(test_db):
        os.remove(test_db)
