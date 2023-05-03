#Importing required packages
import streamlit as st
import requests
from streamlit_chat import message
import openai
import requests

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

st.set_page_config(page_title="Learn Wardley Mapping Bot")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
st.sidebar.markdown("""Welcome to WardleyMapBot! It's great to have you here. To get started, please choose one of the options below:
Type 'Learn' to learn about the components of a Wardley Map.
Type 'Vocabulary' to get a list of common terms and their definitions related to Wardley Mapping.
Type 'Create' to create your own map with step-by-step guidance.
If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!""")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    
def get_initial_message():
    messages = [
        {
            "role": "system",
            "content": f"""
             Interact with WardleyMapBot, your personal guide to learning and creating Wardley Maps.
             Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own map with step-by-step guidance.
             If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!             """
        },
        {
            "role": "user",
            "content": "{question}"
        },
        {
            "role": "assistant",
            "content": ""
        }
    ]
    return messages

def get_chatgpt_response(messages, model=model):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    query = "help?"
    st.session_state['messages'] = get_initial_message()
    
query = st.text_input("Question: ", value="", key="input")

if query:
    with st.spinner("thinking... this can take a while..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.sidebar.write(messages)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
