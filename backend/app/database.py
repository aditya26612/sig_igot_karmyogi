import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any
from app.config import settings

DERIVED_TABLES = ['competency_gaps', 'course_recommendations', 'learning_paths', 'learning_path_items']

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def load_db(con: sqlite3.Connection) -> Dict[str, List[Dict[str, Any]]]:
    """Loads all 26 core tables from the database into an in-memory dictionary."""
    con.row_factory = sqlite3.Row
    names = json.loads(settings.TABLE_ORDER_PATH.read_text(encoding="utf-8"))
    data = {}
    for table_name in names:
        cursor = con.execute(f"SELECT * FROM {table_name}")
        data[table_name] = [dict(row) for row in cursor.fetchall()]
    return data

def save_feedback(con: sqlite3.Connection, D: Dict[str, List[Dict[str, Any]]]):
    """Persists updated competency state, evidence, and derived engine calculations."""
    with con:
        # Clear derived tables
        for t in reversed(DERIVED_TABLES):
            con.execute(f"DELETE FROM {t}")
            
        # Update user competencies
        for x in D.get('user_competencies', []):
            cols = [k for k in x if k not in ('user_id', 'competency_id')]
            set_clause = ', '.join(f"{k} = ?" for k in cols)
            params = [x[k] for k in cols] + [x['user_id'], x['competency_id']]
            con.execute(f"UPDATE user_competencies SET {set_clause} WHERE user_id = ? AND competency_id = ?", params)
            
        # Insert new competency evidence
        for x in D.get('competency_evidence', []):
            cols = list(x.keys())
            placeholders = ', '.join(['?'] * len(cols))
            col_names = ', '.join(cols)
            con.execute(f"INSERT OR IGNORE INTO competency_evidence ({col_names}) VALUES ({placeholders})", list(x.values()))
            
        # Re-populate derived tables
        for t in DERIVED_TABLES:
            for x in D.get(t, []):
                cols = list(x.keys())
                placeholders = ', '.join(['?'] * len(cols))
                col_names = ', '.join(cols)
                con.execute(f"INSERT INTO {t} ({col_names}) VALUES ({placeholders})", list(x.values()))

def init_db():
    """Initializes extension tables for application authentication, transcripts, practice, and assessments."""
    con = get_db_connection()
    with con:
        # 1. Application Users / Auth Credentials
        con.execute("""
        CREATE TABLE IF NOT EXISTS app_users (
            user_id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('ADMIN', 'REVIEWER', 'LEARNER')),
            department TEXT,
            designation TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
        """)
        
        # 2. Transcript Chunks for Search & Quiz Generation
        con.execute("""
        CREATE TABLE IF NOT EXISTS transcript_chunks (
            chunk_id TEXT PRIMARY KEY,
            lesson_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            topic TEXT NOT NULL,
            start_seconds INTEGER DEFAULT 0,
            end_seconds INTEGER DEFAULT 0,
            timestamp_label TEXT NOT NULL,
            text_content TEXT NOT NULL,
            summary TEXT,
            provenance TEXT DEFAULT 'DERIVED'
        )
        """)
        
        # 3. Practice Quizzes (Lesson-level interactive practice)
        con.execute("""
        CREATE TABLE IF NOT EXISTS practice_quizzes (
            quiz_id TEXT PRIMARY KEY,
            lesson_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        
        # 4. Practice Questions
        con.execute("""
        CREATE TABLE IF NOT EXISTS practice_questions (
            question_id TEXT PRIMARY KEY,
            quiz_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            question_text TEXT NOT NULL,
            options_json TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            explanation TEXT NOT NULL,
            chunk_id TEXT,
            timestamp_label TEXT,
            difficulty TEXT DEFAULT 'MEDIUM',
            is_approved INTEGER DEFAULT 1,
            review_status TEXT DEFAULT 'APPROVED',
            FOREIGN KEY (quiz_id) REFERENCES practice_quizzes(quiz_id)
        )
        """)
        
        # 5. Practice Attempts (Learner quiz submissions)
        con.execute("""
        CREATE TABLE IF NOT EXISTS practice_attempts (
            attempt_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            quiz_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            answers_json TEXT NOT NULL,
            topic_breakdown_json TEXT,
            attempted_at TEXT NOT NULL
        )
        """)

        # 5b. Lesson Watch Progress (persisted mark-as-watched per learner)
        con.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            user_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            seconds_watched INTEGER,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (user_id, lesson_id)
        )
        """)
        
        # 6. Assessment Submissions (Formal supervisor-reviewed evidence)
        con.execute("""
        CREATE TABLE IF NOT EXISTS assessment_attempts (
            submission_id TEXT PRIMARY KEY,
            assessment_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            rubric_version TEXT NOT NULL,
            overall_score REAL NOT NULL,
            confidence REAL NOT NULL,
            coverage REAL NOT NULL,
            estimated_level INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('PENDING_REVIEW', 'APPROVED', 'REJECTED')),
            submitted_at TEXT NOT NULL,
            reviewer_id TEXT,
            reviewer_comments TEXT,
            reviewed_at TEXT,
            payload_json TEXT NOT NULL,
            payload_hash TEXT NOT NULL
        )
        """)
        
        # 7. Audit Logs
        con.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id TEXT PRIMARY KEY,
            actor_id TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            details TEXT,
            timestamp TEXT NOT NULL
        )
        """)
        
        # 8. Course Playlists & Video Lessons metadata
        con.execute("""
        CREATE TABLE IF NOT EXISTS curated_playlists (
            playlist_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            youtube_url TEXT NOT NULL,
            channel_name TEXT,
            competency_id TEXT NOT NULL,
            description TEXT,
            category TEXT,
            total_lessons INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ACTIVE'
        )
        """)
        
        con.execute("""
        CREATE TABLE IF NOT EXISTS curated_lessons (
            lesson_id TEXT PRIMARY KEY,
            playlist_id TEXT NOT NULL,
            sequence_no INTEGER NOT NULL,
            title TEXT NOT NULL,
            youtube_video_id TEXT NOT NULL,
            youtube_url TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 15,
            competency_id TEXT NOT NULL,
            has_transcript INTEGER DEFAULT 1,
            FOREIGN KEY (playlist_id) REFERENCES curated_playlists(playlist_id)
        )
        """)

        # RAG: permanent raw caption cache
        con.execute("""
        CREATE TABLE IF NOT EXISTS raw_transcripts (
            lesson_id TEXT PRIMARY KEY,
            transcript_text TEXT,
            language TEXT DEFAULT 'en',
            source TEXT DEFAULT 'YOUTUBE_AUTO',
            fetched_at TEXT,
            status TEXT DEFAULT 'FETCHED'
        )
        """)

        # RAG: local embedding vectors (float32 bytes)
        con.execute("""
        CREATE TABLE IF NOT EXISTS chunk_embeddings (
            chunk_id TEXT PRIMARY KEY,
            embedding BLOB,
            model_name TEXT,
            created_at TEXT
        )
        """)

        # RAG: FTS5 lexical index over transcript chunks
        con.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS transcript_fts USING fts5(
            chunk_id UNINDEXED,
            text_content,
            topic,
            tokenize='unicode61'
        )
        """)

    con.close()
