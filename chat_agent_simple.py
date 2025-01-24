from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
import streamlit as st
import os

# Load data and build index

api_key = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(model="gpt-3.5-turbo", api_key=api_key)
data = SimpleDirectoryReader(input_dir="./data/").load_data()
index = VectorStoreIndex.from_documents(data)

# Configure chat engine

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    llm=llm,
    system_prompt=(
        "You are a helpful chatbot called Flor with access to files containing information about an organization called COCo (Centre for Community Organizations)"
        "You can only discuss details from those documents and hold normal, friendly conversations."
        "Keep your answers concise."
        "If you don’t have enough information to answer a query accurately, indicate that and provide any relevant context you do have."
        "Only when the conversation is complete, close with a friendly message on a line line such as:"
        "'If you ever have more questions in the future, feel free to reach out. Have a great day! 🌻'"
    ),
)


def stream_data(prompt):
    streaming_response = chat_engine.stream_chat(prompt)
    for word in streaming_response.response_gen:
        yield word
