import streamlit as st
import openai

# Set your OpenAI API key here using Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the initial instructions for the assistant
initial_instructions = "You are a helpful assistant."

# Main chat interface
st.title("OpenAI Chat with GPT-4")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to send a message to the Assistant
def send_message(message_text):
    if message_text:  # only send a message if it's not empty
        # Add the user's message to the session state
        st.session_state['messages'].append({'sender': 'User', 'message': message_text})
        
        try:
            # Create the message for the assistant
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": initial_instructions},
                    {"role": "user", "content": message_text}
                ]
            )
            
            # Get the assistant's response
            assistant_message = response.choices[0].message['content']

        except openai.error.OpenAIError as e:
            assistant_message = f"An error occurred: {str(e)}"

        # Add the assistant's response to the session state
        st.session_state['messages'].append({'sender': 'Assistant', 'message': assistant_message})
        
        # Clear the input box after sending
        st.session_state['user_message'] = ""

# Input box for the user to type their message
user_message = st.text_input("Your Message", key="user_message")

# Button to send the message
if st.button("Send") and user_message:
    send_message(user_message)

# Display chat messages
for chat in reversed(st.session_state.messages):
    if chat['sender'] == 'User':
        st.text_area("", value=chat['message'], height=75, key=f"user_{chat['message']}")
    else:
        st.text_area("", value=chat['message'], height=75, key=f"assistant_{chat['message']}", bg_color="#F0F2F6")
