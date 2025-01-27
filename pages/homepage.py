import streamlit as st
import time
import uuid

from chat_agent_complex import stream_data
from database import init_db, load_state_from_db, save_state_to_db


st.title("COCo AI Genie 💡")
st.info("A chatbot that can help you to navigate the legal intricacies of nonprofits and community groups in Quebec", icon="ℹ️")
st.warning("I do not provide legal advice. If you need legal assistance, please contact us at info@coco-net.org for a referral to a lawyer or legal clinic.", icon="⚠️")
