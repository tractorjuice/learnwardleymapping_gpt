# Importing required packages
import streamlit as st
import openai
import uuid
import time

from openai import OpenAI
client = OpenAI()

#MODEL = "gpt-3"
#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-3.5-turbo-0613"
#MODEL = "gpt-3.5-turbo-16k"
#MODEL = "gpt-3.5-turbo-16k-0613"
#MODEL = "gpt-4"
#MODEL = "gpt-4-0613"
#MODEL = "gpt-4-32k-0613"
MODEL = "gpt-4-1106-preview"
#MODEL = "gpt-4-vision-preview"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "error" not in st.session_state:
    st.session_state.error = 1

st.set_page_config(page_title="Learn Wardley Mapping")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.3")
st.sidebar.markdown("Using gpt-4-1106-preview API")
st.sidebar.markdown(st.session_state.session_id)
st.sidebar.divider()

if "assistant" not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Load the previously created assistant
    st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])

    # Create a new thread for this session
    st.session_state.thread = client.beta.threads.create(
        metadata={
            'session_id': st.session_state.session_id,
        }
    )
 
# If the run is completed, display the messages
elif hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
    # Retrieve the list of messages
    st.session_state.messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id
    )

    # Display messages
    for message in reversed(st.session_state.messages.data):
        if message.role in ["user", "assistant"]:
            with st.chat_message(message.role):
                for content_part in message.content:
                    message_text = content_part.text.value
                    st.markdown(message_text)

if prompt := st.chat_input("How can I help you?"):
    with st.chat_message('user'):
        st.write(prompt)

    # Add message to the thread
    st.session_state.messages = client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

    # Do a run to process the messages in the thread
    st.session_state.run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )
    time.sleep(1) # Wait 1 second before checking run status
    st.rerun()
                    
# Check the run status and act accordingly
if hasattr(st.session_state.run, 'status') and st.session_state.run.status == "running":
    with st.chat_message('assistant'):
        st.write("Thinking ......")
    time.sleep(3) # Wait 1 second before checking run status
    st.rerun()

# Check the run status and act accordingly
if hasattr(st.session_state.run, 'status') and st.session_state.run.status == "failed":
    with st.chat_message('assistant'):
        st.write("Run failed, retying ......")
    st.session_state.error += 1
    st.write(st.session_state.error)
    if st.session_state.error < 3   
        time.sleep(3) # Wait 1 second before checking run status
        st.rerun()
    
# Check the run status and act accordingly
if hasattr(st.session_state.run, 'status') and st.session_state.run.status != "completed":
    st.session_state.run = client.beta.threads.runs.retrieve(
        thread_id=st.session_state.thread.id,
        run_id=st.session_state.run.id,
    )
    time.sleep(1) # Wait 1 second before checking run status
    st.rerun()    
