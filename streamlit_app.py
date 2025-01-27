import streamlit as st
from time import sleep

from database import init_db, load_state_from_db, save_state_to_db


# Set the page title and icon
st.set_page_config(
    page_title="COCo AI Genie",
    page_icon="💡"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.rerun()


if st.session_state.logged_in == True:
    pg = st.navigation([
        st.Page("pages/homepage.py", title="COCo AI Genie",
                icon="🤖", default=True),
        st.Page("pages/files.py", title="Documents",
                icon=":material/folder:"),
        st.Page("pages/history.py", title="History", icon=":material/history:")
    ])
    with st.sidebar:
        if st.button("Log out"):
            logout()

else:
    pg = st.navigation([
        st.Page("pages/homepage.py", title="COCo AI Genie",
                icon="🤖", default=True),
        st.Page("pages/login.py", title="Log in", icon=":material/login:")
    ])

pg.run()
