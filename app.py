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
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
#st.sidebar.markdown("## Enter Map ID")
    
def get_initial_message():
    query = "help?"
    #url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    #response = requests.get(url)
    #map_data = response.json()
    #map_text = map_data["text"]
    #st.session_state['map_text'] = map_text
    
    messages = [
        {
            "role": "system",
            "content": f"""
             As a chatbot, Interact with WardleyMapBot, your personal guide to learning and creating Wardley Maps
             Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Create' your own map with step-by-step guidance. If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!
             """
        },
        {
            "role": "user",
            "content": "{question}"
        },
        {
            "role": "assistant",
            "content": """
            Welcome to WardleyMapBot! I'm here to help you learn about and create Wardley Maps. Let's get started.
            Please choose one of the following options by typing it out:
            
            Learn - Learn about the components of a Wardley Map and its uses
            Create - Create your own Wardley Map with step-by-step guidance
            Help - Get assistance with Wardley Maps or this interaction.
            """
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
    st.session_state['messages'] = get_initial_message()
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
#if 'map_text' not in st.session_state:
#    st.session_state['map_text'] = []
    
query = st.text_input("Question: ", value="", key="input")
    
#map_id = st.sidebar.text_input("Enter the ID of the Wardley Map:", value="7OPuuDEWFoyfj00TS1")
#st.sidebar.write("For https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI")
#st.sidebar.write("Examples:\n\ngQuu7Kby3yYveDngy2\n\nxi4JEUqte7XRWjjhgQ\n\nMOSCNj9iXnXdbCutbl\n\nOXeRWhqHSLDXfOnrfI\n\nO42FCNodPW3UPaP8AD")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    
#if st.session_state.get('current_map_id') != map_id:
#    del st.session_state['messages']
#    st.session_state['past'] = []
#    st.session_state['generated'] = []
#    st.session_state['current_map_id'] = map_id
#    query = "Help?"
#    st.session_state['messages'] = get_initial_message()
    
#title = ""

#if 'map_text' in st.session_state:
#    st.sidebar.markdown("### Downloaded Map Data")
#    map_text = st.session_state['map_text']
#    for line in map_text.split("\n"):
#        if line.startswith("title"):
#            title = line.split("title ")[1]
#    if title:
#        st.sidebar.markdown(f"### {title}")
#    st.sidebar.code(st.session_state['map_text'])

if query:
    with st.spinner("thinking... this can take a while..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        #del st.session_state["input"]

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
