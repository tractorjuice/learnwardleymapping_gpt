#Importing required packages
import streamlit as st
import openai
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks import get_openai_callback

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
#MODEL = "gpt-3"
#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-3.5-turbo-0613"
#MODEL = "gpt-3.5-turbo-16k"
#MODEL = "gpt-3.5-turbo-16k-0613"
MODEL = "gpt-4"
#MODEL = "gpt-4-0613"
#MODEL = "gpt-4-32k-0613"

st.set_page_config(page_title="Learn Wardley Mapping Bot")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.0")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.divider()
    
def get_initial_message():
    messages = [
        {
            "role": "system",
            "content": f"""
             Interact with WardleyMapBot, your personal guide to learning and creating Wardley Maps.
             Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own map with step-by-step guidance.
             If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!
             """
        },
        {
            "role": "user",
            "content": "Help?"
        },
        {
            "role": "assistant",
            "content": """
            I'm here to help you learn about and create Wardley Maps. Here are some options for getting started: 1. Learn: To learn about the components and concepts of a Wardley Map, type "Learn". 2. Vocabulary: To get a list of common Wardley Map terms and their definitions, type "Vocabulary". 3. Create: To create your own Wardley Map with step-by-step guidance, type "Create". If you have any specific questions or need clarification on any aspect of Wardley Mapping, feel free to ask.            """
        }
    ]
    return messages

def get_chatgpt_response(messages, model=MODEL):
    
    # Convert messages to corresponding SystemMessage, HumanMessage, and AIMessage objects
    new_messages = []
    for message in messages:
        role = message['role']
        content = message['content']
        
        if role == 'system':
            new_messages.append(SystemMessage(content=content))
        elif role == 'user':
            new_messages.append(HumanMessage(content=content))
        elif role == 'assistant':
            new_messages.append(AIMessage(content=content))
    
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name=model,
        temperature=0.0,
    )
    try:
        with get_openai_callback() as cb:
            response = chat(new_messages)
    except:
        st.error("OpenAI Error")
    if response is not None:
        return response.content
    else:
        st.error("Error")
        return "Error: response not found"

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
            "role": "system",
            "content": f"""
             Interact with WardleyMapBot, your personal guide to learning and creating Wardley Maps.
             Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own map with step-by-step guidance.
             If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!
             """
        },
        {
            "role": "user",
            "content": "Help?"
        },
        {
            "role": "assistant",
            "content": """
            I'm here to help you learn about and create Wardley Maps. Here are some options for getting started: 1. Learn: To learn about the components and concepts of a Wardley Map, type "Learn". 2. Vocabulary: To get a list of common Wardley Map terms and their definitions, type "Vocabulary". 3. Create: To create your own Wardley Map with step-by-step guidance, type "Create". If you have any specific questions or need clarification on any aspect of Wardley Mapping, feel free to ask.            """
        })
    

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})




#query = st.text_input("Question: ", value="", key="input")

#if 'generated' not in st.session_state:
#    st.session_state['generated'] = []
  
#if 'past' not in st.session_state:
#    st.session_state['past'] = []

#if 'messages' not in st.session_state:
#    st.session_state['messages'] = get_initial_message()
#    st.session_state.past.append("Help?")
#    st.session_state.generated.append("""
#    I'm here to help you learn about and create Wardley Maps. Here are some options for getting started:\n\n1. Learn: To learn about the components and concepts of a Wardley Map, type "Learn". \n2. Vocabulary: To get a list of common Wardley Map terms and their definitions, type "Vocabulary". \n3. Create: To create your own Wardley Map with step-by-step guidance, type "Create". \n\nIf you have any specific questions or need clarification on any aspect of Wardley Mapping, feel free to ask.
#    """)

#if query:
#    with st.spinner("thinking... this can take a while..."):
#        messages = st.session_state['messages']
#        messages = update_chat(messages, "user", query)
#        response = get_chatgpt_response(messages, MODEL)
#        messages = update_chat(messages, "assistant", response)
#        st.session_state.past.append(query)
#        st.session_state.generated.append(response)

#if st.session_state['generated']:
#    for i in range(len(st.session_state['generated'])-1, -1, -1):
#        message(st.session_state["generated"][i], key=str(i))
#        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
