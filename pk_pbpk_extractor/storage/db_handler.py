"""
storage/db_handler.py — Dual-backend database handler.

Backends:
  - "supabase"  → Supabase Python client (REST API over HTTPS, no port issues)
  - "sqlite"    → Local SQLite (default dev fallback)

Set DB_BACKEND=supabase in .env
"""

import json
import os
import sqlite3
from datetime import datetime
from contextlib import contextmanager

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
except ImportError:
    pass

DB_BACKEND   = os.environ.get("DB_BACKEND", "sqlite").lower()
SQLITE_PATH  = os.environ.get("SQLITE_PATH", "pk_parameters.db")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")

_supabase_client = None

def _get_supabase():
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SECRET_KEY must be set in .env"
            )
        from supabase import create_client
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


# ─────────────────────────────────────────────────────────────
# SQLite context manager (local dev only)
# ─────────────────────────────────────────────────────────────

@contextmanager
def _sqlite_conn():
    path = SQLITE_PATH.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────
# Schema setup
# ─────────────────────────────────────────────────────────────

def setup_database():
    if DB_BACKEND == "supabase":
        sb = _get_supabase()
        # Create tables via RPC if they don't exist.
        # Supabase free tier requires tables created via Dashboard or SQL editor.
        # We'll attempt to create them via the REST SQL endpoint.
        sql = """
        CREATE TABLE IF NOT EXISTS documents (
            paper_id TEXT PRIMARY KEY,
            title TEXT,
            metadata_json TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS pk_parameters (
            id BIGSERIAL PRIMARY KEY,
            paper_id TEXT REFERENCES documents(paper_id),
            table_id TEXT,
            species TEXT,
            formulation TEXT,
            route TEXT,
            dose DOUBLE PRECISION,
            parameter_name TEXT,
            canonical_name TEXT,
            value DOUBLE PRECISION,
            start_value DOUBLE PRECISION,
            end_value DOUBLE PRECISION,
            deviation_value DOUBLE PRECISION,
            measure_type TEXT,
            unit TEXT,
            extracted_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        try:
            result = sb.rpc("exec_sql", {"query": sql}).execute()
            print("  [DB] Supabase schema created via RPC.")
        except Exception:
            # Tables may already exist or RPC not available — try a probe query
            try:
                sb.table("documents").select("paper_id").limit(1).execute()
                print("  [DB] Supabase tables already exist ✅")
            except Exception as e:
                print(f"  [DB] ⚠️  Tables may not exist yet. Please run setup SQL in Supabase Dashboard.")
                print(f"       Error: {e}")
    else:
        with _sqlite_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT,
                    metadata_json TEXT,
                    created_at TIMESTAMP
                )""")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pk_parameters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT,
                    table_id TEXT,
                    species TEXT,
                    formulation TEXT,
                    route TEXT,
                    dose REAL,
                    parameter_name TEXT,
                    canonical_name TEXT,
                    value REAL,
                    start_value REAL,
                    end_value REAL,
                    deviation_value REAL,
                    measure_type TEXT,
                    unit TEXT,
                    source_pass TEXT DEFAULT 'xml_table',
                    FOREIGN KEY(paper_id) REFERENCES documents(paper_id)
                )""")
            # Migrate: add source_pass column if it doesn't exist yet
            try:
                cur.execute("ALTER TABLE pk_parameters ADD COLUMN source_pass TEXT DEFAULT 'xml_table'")
            except Exception:
                pass  # column already exists
        print(f"  [DB] SQLite schema ready at {SQLITE_PATH}")


# ─────────────────────────────────────────────────────────────
# CRUD — upsert document
# ─────────────────────────────────────────────────────────────

def upsert_document(paper_id: str, title: str, metadata: dict):
    meta_str = json.dumps(metadata)
    if DB_BACKEND == "supabase":
        sb = _get_supabase()
        sb.table("documents").upsert({
            "paper_id":      paper_id,
            "title":         title,
            "metadata_json": meta_str,
        }, on_conflict="paper_id").execute()
    else:
        with _sqlite_conn() as conn:
            conn.execute("""
                INSERT INTO documents (paper_id, title, metadata_json, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(paper_id) DO UPDATE SET
                    title=excluded.title, metadata_json=excluded.metadata_json
            """, (paper_id, title, meta_str, datetime.now().isoformat()))


# ─────────────────────────────────────────────────────────────
# CRUD — insert PK parameters
# ─────────────────────────────────────────────────────────────

def insert_pk_parameters(params_list: list):
    if not params_list:
        return

    if DB_BACKEND == "supabase":
        sb = _get_supabase()
        # Assume params_list is already a list of dicts!
        rows = []
        for p in params_list:
            if isinstance(p, dict):
                rows.append(p)
            else:
                # Fallback for old tuples if they ever happen
                row = {
                    "paper_id":        p[0],
                    "table_id":        p[1],
                    "species":         p[2],
                    "formulation":     p[3],
                    "route":           p[4],
                    "dose":            p[5],
                    "parameter_name":  p[6],
                    "canonical_name":  p[7],
                    "value":           p[8],
                    "deviation_value": p[9],
                    "measure_type":    p[10],
                    "unit":            p[11],
                }
                if len(p) >= 13:
                    row["source_pass"] = p[12]
                rows.append(row)
                
        sb.table("pk_parameters").insert(rows).execute()
        print(f"  [DB] Inserted {len(rows)} rows into Supabase pk_parameters ✅")
    else:
        with _sqlite_conn() as conn:
            # We don't care about SQLite for this project currently, but we can add a basic implementation for dicts
            tuples = []
            for p in params_list:
                if isinstance(p, dict):
                    tuples.append((
                        p.get("paper_id"), p.get("table_id"), p.get("species"), p.get("formulation"), 
                        p.get("route"), p.get("dose"), p.get("parameter_name"), p.get("canonical_name"), 
                        p.get("value"), p.get("start_value"), p.get("end_value"), p.get("deviation_value"), p.get("measure_type"), p.get("unit"), 
                        p.get("source_pass", "xml_table"), p.get("compound"), p.get("cohort_or_condition")
                    ))
            if tuples:
                conn.executemany("""
                    INSERT INTO pk_parameters (
                        paper_id, table_id, species, formulation, route, dose,
                        parameter_name, canonical_name, value, start_value, end_value, deviation_value,
                        measure_type, unit, source_pass, compound, cohort_or_condition
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuples)
        print(f"  [DB] Inserted {len(params_list)} rows into SQLite.")


def delete_paper_data(paper_id: str):
    """Remove all existing records for a paper before re-processing."""
    if DB_BACKEND == "supabase":
        sb = _get_supabase()
        sb.table("pk_parameters").delete().eq("paper_id", paper_id).execute()
        sb.table("documents").delete().eq("paper_id", paper_id).execute()
        print(f"  [DB] Cleared existing Supabase records for: {paper_id}")
    else:
        with _sqlite_conn() as conn:
            conn.execute("DELETE FROM pk_parameters WHERE paper_id = ?", (paper_id,))
            conn.execute("DELETE FROM documents WHERE paper_id = ?", (paper_id,))
        print(f"  [DB] Cleared existing SQLite records for: {paper_id}")


def fetch_parameters(paper_id: str = None) -> list[dict]:
    if DB_BACKEND == "supabase":
        sb = _get_supabase()
        q = sb.table("pk_parameters").select("*")
        if paper_id:
            q = q.eq("paper_id", paper_id)
        result = q.limit(1000).execute()
        return result.data or []
    else:
        with _sqlite_conn() as conn:
            cur = conn.cursor()
            if paper_id:
                cur.execute("SELECT * FROM pk_parameters WHERE paper_id = ?", (paper_id,))
            else:
                cur.execute("SELECT * FROM pk_parameters ORDER BY id DESC LIMIT 1000")
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
