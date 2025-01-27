import streamlit as st
from time import sleep

import streamlit as st


st.title("Welcome to Diamond Corp")

st.info("Please log in to continue.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username == "test" and password == "test":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
    else:
        st.error("Incorrect username or password")
    st.rerun()
