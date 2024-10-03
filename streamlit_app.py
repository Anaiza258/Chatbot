from itertools import zip_longest 
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

openapi_key = st.secrets["OPENAI_API_KEY"]

#set streamlit page configuration 
st.set_page_config(page_title = "Hope To Do Or Build ChatBot")
st.title("AI Mentor") 

#initialize session state variable
if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  #store the latest user input
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # store ai generated response
if 'past' not in st.session_state:
    st.session_state['past'] = [] # user past input
    
    #define function to submit that session states
def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input
    #clear prompt input
    st.session_state.prompt_input = ""

# build model for chat
 
chat = ChatOpenAI(
    temperature = 0.5,
    model_name = 'gpt-3.5-turbo',
    openai_api_key = openapi_key,
    max_tokens = 100
)

# Take or write some constraints or guardrails 
def build_message_list():
    """
    Build a list of messages including system, human, AI messages.
    """
    #start ziped message with the system msg
    zipped_messages = [SystemMessage(
        # content = "You are helpful ai mentor talking with human . If you do not know an answer , just say 'I don't know' do not make up an answer"
        content = """Your name is AI Mentor . You are an  AI Technical Expert for Artifical Intelligence, here to guide and assist students  with their AI related questions and concerns . Please provide accurate and helpful information, and always maintain a polite and  professional tone .

                1. Greet the user politely ask user name and ask how you can assist them with AI-related queries.
                2. Provide informative and relevant responses to questions about artifical intelligence, machine learning , deep learning , natural language processing, computer vision, and related topics.
                3. you must Avoid discussing  sensitive, offensive, or harmful content .Refrain from engaging in any form of discrimination, harassment,  or inappropriate behavior.
                4. If the user asks about a  topic unrelated to AI, politely steer the conversation back to AI or  inform them that the topic is outside the scope of this conversation.
                5. Be patient and considerate when responding to user queries, and provide clear explanations.
                6. If the user expresses gratitude or indicates the end of the conversation, respond with polite farewell.
                7. Do Not generate the long paragraphs  in response . Maximum Words should be 100.

                Remember your primary goal  is to assist and educate students in the field of Artifical Intelligence. Always prioritize their learning experience and well-being."""
    )]
# zip together  the past and generated messages 
    for  human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
         if human_msg is not None:
             zipped_messages.append(HumanMessage(
            content=human_msg))
         if ai_msg is not None:
            zipped_messages.append(AIMessage(
            content = ai_msg))   
    return zipped_messages      

def generate_response():
    """
    generate AI response using the ChatOpenAI model.
    """
    #build messages list
    zipped_messages = build_message_list()
    
    #generate response using ai model
    ai_response = chat(zipped_messages)
    
    response=ai_response.content
    return response 

# create text input for user
st.text_input('You: ', key = 'prompt_input', on_change=submit)

if st.session_state.entered_prompt !="":
    # get user query 
    user_query= st.session_state.entered_prompt

    #append user query to past queries
    st.session_state.past.append(user_query)
    
    #generate rsponse 
    output = generate_response()

    #append ai responses to generated responses
    st.session_state.generated.append(output)

#display chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        #display ai response
        message(st.session_state["generated"][i], key=str(i))
        #display user message   
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')