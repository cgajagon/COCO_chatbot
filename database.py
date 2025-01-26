import streamlit as st
import sqlite3
import json
import datetime
import os

DB_PATH = "coco_chat_queries.db"


def init_db():
    """Create the database and user_state table if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_state (
                user_id TEXT PRIMARY KEY,
                state_json TEXT,
                updated_at TIMESTAMP
            )
            """
        )


def load_state_from_db(user_id="default_user"):
    """
    Load session state (as a JSON blob) from the database.
    Returns a dict of the saved state or an empty dict if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT state_json FROM user_state WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if result is not None:
            state_json = result[0]
            # Convert JSON to a Python dict
            return json.loads(state_json)
        else:
            return {}


def save_state_to_db(user_id="default_user", state=None):
    """
    Save the given dict `state` (session_state) to the database as JSON.
    """
    if state is None:
        state = {}

    state_json = json.dumps(state)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO user_state (user_id, state_json, updated_at)
            VALUES (?, ?, ?)
            """,
            (user_id, state_json, datetime.datetime.now())
        )
        conn.commit()
