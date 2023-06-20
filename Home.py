import streamlit as st
from langchain import SQLDatabase
from langchain.chat_models import ChatOpenAI
import openai
# Dotenv library break the app when it is deployed to Stremlit community cloud
# from dotenv import load_dotenv, find_dotenv
import os
from text_to_sql_to_text import TextToSQLToTextChain
from text_to_chart import print_chart_to_screen

# we load the env variables
# load_dotenv(): This function is responsible for loading the environment variables from the env 
# file into the Python script's environment
# _ is typically used as a placeholder variable when the actual value is not needed
#_ = load_dotenv(find_dotenv())

#openai_api_key = os.environ['OPENAI_API_KEY']
#database_uri = os.environ['DATABASE_URI']
openai_api_key = None
database_uri = None
database_connection = None

st.title('Text to SQL to text')

st.markdown("<p style='font-size: 22px;'>Some queries you can try:</p>", unsafe_allow_html=True)

st.markdown("<p style='font-size: 18px;'>When was last time user tomas.gil@agileengine.com watch a video?</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px;'>How many courses do we have?</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px;'>Who are the three student with most videos watched in the last 60 days?</p>", unsafe_allow_html=True)
# if openai_api_key is null, then we ask the user to input the key
# if openai_api_key is not null, then we do not display the input box
if openai_api_key is None:
  openai_api_key = st.text_input("Enter your open ai api key")

# if database_uri is null, then we ask the user to input the key
# if database_uri is not null, then we do not display the input box
if database_uri is None:
  database_uri = st.text_input("Enter your database uri")

def create_database_connection(database_uri):
    global database_connection
    if database_connection is None:
        schema = "lms"
        include_tables = ['chapters',
                'courses',
                'user_courses',
                'user_video_progress',
                'users',
                'videos']
        # Create a database connection
        database_connection = SQLDatabase.from_uri(database_uri, schema=schema, include_tables=include_tables)

@st.cache_resource  # 👈 Add the caching decorator
def load_model():
    # we load the model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)
    return llm

@st.cache_resource  # 👈 Add the caching decorator
def load_chain(_llm, _db):
    chain = TextToSQLToTextChain(_llm, _db)
    return chain

@st.cache_data
def run_query(query):
    response = chain.run(query)
    st.write(response)
    return response

@st.cache_data
def print_chart(text):
    print_chart_to_screen(text)

# if openai_api_key and database_uri are not None, then we load the chain
if openai_api_key != "" and database_uri != "":
    os.environ['OPENAI_API_KEY'] = openai_api_key
    openai.api_key = openai_api_key
    create_database_connection(database_uri=database_uri)
    llm = load_model()
    chain = load_chain(_llm=llm, _db=database_connection)
    query = st.text_input("Enter your query", "")
    # if user entered a query, then we run the query
    if query:
        response = run_query(query)
        # display a button to ask the user if want the query result to be displayed as chart
        if st.button("Display as chart"):
            print_chart(text=response)