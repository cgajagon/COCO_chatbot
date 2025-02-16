import json
import datetime
from sqlalchemy.sql import text
import streamlit as st
import pandas as pd


def init_db(conn):
    """Create the database and user_state table if they don't exist."""
    with conn.session as s:
        s.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS user_state (
                    user_id TEXT PRIMARY KEY,
                    state_json TEXT,
                    updated_at TIMESTAMP
                );
                """
            )
        )
    s.commit()

        s.commit()


def load_state_from_db(conn, user_id="default_user"):
    """
    Load session state (as a JSON blob) from the database.
    Returns a dict of the saved state or an empty dict if not found.
    """
    with conn.session as s:
        result = s.execute(
            "SELECT state_json FROM user_state WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if result is not None:
            state_json = result[0]
            # Convert JSON to a Python dict
            return json.loads(state_json)
        else:
            return {}


def save_state_to_db(conn, user_id="default_user", state=None):
    """
    Save the given dict `state` (session_state) to the database as JSON.
    """
    if state is None:
        state = {}

    state_json = json.dumps(state)
    with conn.session as s:
        s.execute(
            text(
                """
                INSERT OR REPLACE INTO user_state (user_id, state_json, updated_at)
                VALUES (:user_id, :state_json, :updated_at)
                """
            ),
            {
                "user_id": user_id,
                "state_json": state_json,
                "updated_at": datetime.datetime.now(),
            }
        )
        s.commit()


def fetch_data(conn, initial_date, end_date):
    """
    Fetch data from the database between initial_date and end_date.

    Parameters:
        conn: Streamlit connection object.
        initial_date (str or datetime): Start date (inclusive).
        end_date (str or datetime): End date (inclusive).

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    query = """
        SELECT * FROM user_state
        WHERE updated_at BETWEEN :initial_date AND :end_date
    """

    try:
        # Use conn.session and execute the query
        with conn.session as s:
            result = s.execute(
                text(query),
                {"initial_date": initial_date, "end_date": end_date},
            )
            # Fetch all results and convert them to a DataFrame
            rows = result.fetchall()
            columns = result.keys()  # Get column names
            df = pd.DataFrame(rows, columns=columns)

        # Optionally, parse state_json to pretty format
        if "state_json" in df.columns:
            df["state_json"] = df["state_json"].apply(
                lambda x: json.dumps(json.loads(x), indent=2)
            )
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()
