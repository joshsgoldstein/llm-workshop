import streamlit as st
import uuid
from api_controller import APIController

st.title("Seldon Chatbot Using the OpenAi Runtime")

# Sidebar for selecting the target LLM
with st.sidebar:
    target = st.selectbox(
        "Choose the target LLM",
        options=['local', 'openai'],
        index=1,  # Default selection; adjust as needed
        help="The target LLM. Choices: local, openai"
    )

    # Generate a unique memory ID if one does not already exist in the session state
    if 'memory_id' not in st.session_state:
        st.session_state.memory_id = str(uuid.uuid4())
    
    # Display the memory ID for user reference
    memory_id_display = st.text_input("Memory ID:", value=st.session_state.memory_id, help="Memory ID of conversation", disabled=True)

# Initialize the API controller with the chosen target and the session's memory ID
api_controller = APIController(session=st.session_state.memory_id, target=target)

# Initialize session state for storing messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = api_controller.sync_send(prompt)
        print(response)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})