import sqlite3
import pandas as pd

# 1. Connect to SQLite database
connection = sqlite3.connect("coco_chat_queries.db")

# 2. Write a query to select the data you want
query = """
SELECT user_id, state_json
FROM user_state
"""

# 3. Load data into a pandas DataFrame
df = pd.read_sql_query(query, connection)

# Close the connection if you do not need it anymore
connection.close()

# Inspect the first few rows
df.to_csv('user_state.csv', index=False)
