import streamlit as st
import time

from chat_agent_complex import stream_data

# Set the page title and icon
st.set_page_config(
    page_title="COCo AI Genie",
    page_icon="💡"
)

st.title("COCo AI Genie 💡")
st.info("A chatbot that can help you yo navigate the legal intricacies of nonprofits and community groups in Quebec", icon="ℹ️")
st.warning("I do not provide legal advice. If you need legal assistance, please contact us at info@coco-net.org for a referral to a lawyer or legal clinic.", icon="⚠️")

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
            print(f"The response is: {response}")
        # Save assistant's response in session state
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

        if "Have a great day!" in response:  # End the conversation and start the feedback flow
            st.session_state.conversation_end = True
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
            st.rerun()

    if "vote" not in st.session_state:
        feedback()
    else:
        st.markdown(
            f"Thank you for your feedback! You rated your experience as {
                st.session_state.vote['selected']} stars. 🌟"
        )
