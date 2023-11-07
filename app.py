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

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = []
    
st.set_page_config(page_title="Learn Wardley Mapping")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.1")
st.sidebar.markdown("Using gpt-4-1106-preview API")
st.sidebar.markdown(st.session_state.session_id)
st.sidebar.divider()
# Check if the user has provided an API key, otherwise default to the secret

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "assistant" not in st.session_state:
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
st.sidebar.write("Assistant: ", st.session_state.assistant)

if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()

if prompt := st.chat_input("How can I help you?"):
    st.write(f"User has sent the following prompt: {prompt}")

    message = client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )
    st.sidebar.write("Message: ", message)

    st.session_state.run = client.beta.threads.runs.create(
      thread_id=st.session_state.thread.id,
      assistant_id=st.session_state.assistant.id,
      instructions="What is Inertia?"
    )
    st.sidebar.write("Run 1: ", st.session_state.run)
    
    run = client.beta.threads.runs.retrieve(
      thread_id=st.session_state.thread.id,
      run_id=st.session_state.run.id
    )
    st.sidebar.write("Run 2: ", run)
    
    thread_messages = openai.beta.threads.messages.list(st.session_state.thread.id)
    st.sidebar.write("Messages: ", thread_messages.data)
    
    messages = client.beta.threads.messages.list(
      thread_id=st.session_state.thread.id
    )
    
    #st.write("Messages: ", messages)
    
    # Let's assume `thread_messages` is the SyncCursorPage[ThreadMessage] object containing your data
    
    # Assuming `thread_messages` is your SyncCursorPage[ThreadMessage] object containing your data
    
    # Iterate over each ThreadMessage object in the data list
    #for message in messages.data:
    #    for content_part in message.content:
    #        # Assuming that 'content_part' is a MessageContentText object with an attribute 'text'
    #        # which in turn is an object with an attribute 'value' that contains the actual message text
    #        message_text = content_part.text.value
    #        st.write(f"{message.role} said: {message_text}")#


    #for message in messages.data:
    #    if message["role"] in ["user", "assistant"]:
    #        with st.chat_message(message["role"]):
    #            st.markdown(message["content"])


    for message in messages.data:
        # Check if the message role is either 'user' or 'assistant'
        if message.role in ["user", "assistant"]:
            with st.chat_message(message["role"]):
                for content_part in message.content:
                    message_text = content_part.text.value
                    st.markdown(message_text)


