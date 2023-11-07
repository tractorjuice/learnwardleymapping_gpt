#Importing required packages
import streamlit as st
import openai
import uuid

from openai import OpenAI
client = OpenAI()

#MODEL = "gpt-3"
#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-3.5-turbo-0613"
#MODEL = "gpt-3.5-turbo-16k"
#MODEL = "gpt-3.5-turbo-16k-0613"
#MODEL = "gpt-4"
#MODEL = "gpt-4-0314" # Legacy
#MODEL = "gpt-4-0613"
#MODEL = "gpt-4-32k-0314" # Legacy
#MODEL = "gpt-4-32k-0613"
MODEL = "gpt-4-1106-preview"
#MODEL = "gpt-4-vision-preview"
   
st.set_page_config(page_title="Learn Wardley Mapping")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.1")
st.sidebar.markdown("Using gpt-4-1106-preview API")
st.sidebar.markdown(st.session_state.session_id)
st.sidebar.divider()
# Check if the user has provided an API key, otherwise default to the secret

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid())
   
if "run" not in st.session_state:
    st.session_state.run = []

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "assistant" not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.session_state.assistant = client.beta.assistants.create(
        name="Learn Wardley Mapping",
        instructions="""
            Interact with LearnWardleyMapping, your personal guide to learning and creating Wardley Maps.
            Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own map with step-by-step guidance.
            If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!
            """,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )

if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()

if prompt := st.chat_input("How can I help you?"):
    with st.chat_message('user'):
        st.write(prompt)

    st.session_state.messages = client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

# Check if the run has not completed, and if not, create one
if st.session_state.run.get("status") != "completed":
    run_response = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )
    # Update the run in session state
    st.session_state.run = run_response
    # Use st.rerun() to update the page with the new run status
    st.rerun()

# If the run is completed, display the messages
if st.session_state.run.get("status") == "completed":
    # Retrieve the list of messages
    messages_response = client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id
    )
    # Update the messages in session state
    st.session_state.messages = messages_response.data

    # Display messages
    for message in st.session_state.messages:
        if message.role in ["user", "assistant"]:
            with st.chat_message(message.role):
                for content_part in message.content:
                    message_text = content_part.text.value
                    st.markdown(message_text)
