import streamlit as st
import pandas as pd
from io import StringIO
import datetime

from database import fetch_data

# Create a connection to the database
conn = st.connection('sessions_db', type='sql')

# Function to convert DataFrame to CSV


def convert_df_to_csv(df):
    """Convert DataFrame to CSV string."""
    return df.to_csv(index=False).encode('utf-8')


# Streamlit App Layout
st.title("Sessions viewer and CSV Downloader")
st.subheader("Filtered Data")


# Sidebar for filters
st.sidebar.header("Filter Options")

updated_at_from = st.sidebar.date_input(
    "Sessions from",
    value=datetime.date.today() - datetime.timedelta(days=30),
    max_value=datetime.date.today()
)
updated_at_to = st.sidebar.date_input(
    "Session To",
    value=datetime.date.today(),
    max_value=datetime.date.today()
)

# Prepare filter dictionary
filters = {}
if updated_at_from:
    filters["updated_at_from"] = datetime.datetime.combine(
        updated_at_from, datetime.time.min)
if updated_at_to:
    filters["updated_at_to"] = datetime.datetime.combine(
        updated_at_to, datetime.time.max)

# Fetch and display data
df = fetch_data(
    conn,
    str(filters['updated_at_from']),
    str(filters['updated_at_to'])
)

if df.empty:
    st.info("No records found with the applied filters.")
else:
    # Improve display of the state_json column
    if 'state_json' in df.columns:
        df_display = df.copy()
        df_display['state_json'] = df_display['state_json'].apply(
            lambda x: x.replace('\n', '<br>'))
        st.markdown(df_display.to_html(escape=False, index=False),
                    unsafe_allow_html=True)
    else:
        st.dataframe(df)

    # Download button
    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_user_state.csv',
        mime='text/csv',
    )
