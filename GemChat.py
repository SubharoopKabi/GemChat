from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
# import json 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

#initialize streamlit app

st.header("Converse with GemChat🤖")


if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

# Add custom CSS to align the button
st.markdown(
    """
    <style>

    #bui2__anchor{
       margin-top: 28px;
    }
    .button {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create input text box and button side by side in a fixed container
input_container = st.container()
response_container = st.container()
# Create input text box and button side by side

with input_container:
    col1, col2 = st.columns([4, 1])
    with col1:
        input = st.text_input("Input:", key="input")
    with col2:
        submit = st.button("Chat→", key="submit", help="Ask the question", type="primary")

with response_container:
    if submit and input:
        response = get_gemini_response(input)
 
        ## Add user query and response to session chat history 
        st.session_state['chat_history'].append(("You",input))


        bot_response=""
        for chunk in response:
            if "```" in chunk.text:
                st.code(chunk.text.replace("```", ""), language='python')
            else:
                st.write(chunk.text)
            bot_response+=chunk.text
        st.session_state['chat_history'].append(("Bot", bot_response))




def save_chat_history():
    chat_history_lines = [f"{role}: {text}" for role, text in st.session_state['chat_history']]
    chat_history_str = "\n".join(chat_history_lines)
    return chat_history_str

chat_history_str = save_chat_history()

# Create a download button
st.download_button(
    label="Download Chat History",
    data=chat_history_str,
    file_name='chat_history.txt',
    mime='application/txt'
)