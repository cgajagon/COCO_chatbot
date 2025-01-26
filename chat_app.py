import streamlit as st
import time
import uuid

from chat_agent_complex import stream_data
from database import init_db, load_state_from_db, save_state_to_db


# Set the page title and icon
st.set_page_config(
    page_title="COCo AI Genie",
    page_icon="💡"
)

st.title("COCo AI Genie 💡")
st.info("A chatbot that can help you to navigate the legal intricacies of nonprofits and community groups in Quebec", icon="ℹ️")
st.warning("I do not provide legal advice. If you need legal assistance, please contact us at info@coco-net.org for a referral to a lawyer or legal clinic.", icon="⚠️")

# Create a connection to the database and initialize the DB (creates the file and table if not present)
conn = st.connection('sessions_db', type='sql')
init_db(conn)

# Initialize and generate a random user_id.
if "user_id" not in st.session_state:
    # Generate a random UUID (shortening it to 8 characters for convenience).
    st.session_state.user_id = str(uuid.uuid4())[:8]

# Initialize the conversation messages if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    icon = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# Add a greeting message from the Assistant if the conversation is new
if not st.session_state.messages:
    initial_greeting = "Hello! I'm Flor, your AI guide. How can I help you today? 🌻"
    st.session_state.messages.append(
        {"role": "assistant", "content": initial_greeting})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(initial_greeting)

if "conversation_end" not in st.session_state:
    # Handle user input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generate and display assistant's response
        with st.chat_message("assistant", avatar="🤖"):
            stream = stream_data(prompt)
            response = st.write_stream(stream)
        # Save assistant's response in session state
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

        if "Have a great day!" in response:  # End the conversation and start the feedback flow
            st.session_state.conversation_end = True
            # Save the session state to the database
            session_dict = dict(st.session_state)
            save_state_to_db(conn, st.session_state.user_id, session_dict)
            time.sleep(1)
            st.rerun()

else:  # Feedback flow
    @st.dialog("How was your experience?")
    def feedback():
        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        reason = st.text_input("Any feedback?")
        if st.button("Submit"):
            if selected is not None:
                st.session_state.vote = {
                    "selected": sentiment_mapping[selected], "reason": reason}
            # Save the session state to the database
            session_dict = dict(st.session_state)
            save_state_to_db(conn, st.session_state.user_id, session_dict)
            st.rerun()

    if "vote" not in st.session_state:
        feedback()
    else:
        st.markdown(
            f"Thank you for your feedback! You rated your experience as {
                st.session_state.vote['selected']} stars. 🌟"
        )
