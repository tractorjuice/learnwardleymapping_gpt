# Importing required packages
import streamlit as st
import openai
import uuid
import time

from openai import OpenAI
client = OpenAI()

# gpt-3.5-turbo, gpt-4, and gpt-4-turbo-preview point to the latest model version
#MODEL = "gpt-3.5-turbo" # 4K, Sept 2021. Legacy. Currently points to gpt-3.5-turbo-0613.
#MODEL = "gpt-3.5-turbo-16k" # 16K, Sept 2021. Legacy. Snapshot of gpt-3.5-turbo from June 13th 2023. Will be deprecated on June 13, 2024
MODEL = "gpt-3.5-turbo-1106" # 16K, Sept 2021. New Updated GPT 3.5 Turbo. The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.
#MODEL = "gpt-4" # 8K, Sept 2021
#MODEL = "gpt-4-32k" # 32K, Sept 2021
#MODEL = "gpt-4-turbo-preview" # 128K, Apr 2023
#MODEL = "gpt-4-1106-preview" # 128K, Apr 2023

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0

st.set_page_config(page_title="Learn Wardley Mapping")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.image("./logo.png")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.3")
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

    for thread_message in st.session_state.messages.data:
        for message_content in thread_message.content:
            # Access the actual text content
            message_content = message_content.text
            annotations = message_content.annotations
            citations = []
            
            # Iterate over the annotations and add footnotes
            for index, annotation in enumerate(annotations):
                # Replace the text with a footnote
                message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
            
                # Gather citations based on annotation attributes
                if (file_citation := getattr(annotation, 'file_citation', None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
                elif (file_path := getattr(annotation, 'file_path', None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
                    # Note: File download functionality not implemented above for brevity

            # Add footnotes to the end of the message before displaying to user
            message_content.value += '\n' + '\n'.join(citations)

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
    if st.session_state.retry_error < 3:
        time.sleep(1) # Wait 1 second before checking run status
        st.rerun()
                    
# Check if 'run' object has 'status' attribute
if hasattr(st.session_state.run, 'status'):
    # Handle the 'running' status
    if st.session_state.run.status == "running":
        with st.chat_message('assistant'):
            st.write("Thinking ......")
        if st.session_state.retry_error < 3:
            time.sleep(1)  # Short delay to prevent immediate rerun, adjust as needed
            st.rerun()

    # Handle the 'failed' status
    elif st.session_state.run.status == "failed":
        st.session_state.retry_error += 1
        with st.chat_message('assistant'):
            if st.session_state.retry_error < 3:
                st.write("Run failed, retrying ......")
                time.sleep(3)  # Longer delay before retrying
                st.rerun()
            else:
                st.error("FAILED: The OpenAI API is currently processing too many requests. Please try again later ......")

    # Handle any status that is not 'completed'
    elif st.session_state.run.status != "completed":
        # Attempt to retrieve the run again, possibly redundant if there's no other status but 'running' or 'failed'
        st.session_state.run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=st.session_state.run.id,
        )
        if st.session_state.retry_error < 3:
            time.sleep(3)
            st.rerun()
