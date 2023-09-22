import os
import streamlit as st
import pandas as pd
import openai
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
# from langchain.agents import create_pandas_dataframe_agent
# from langchain.agents.agent_types import AgentType

from tempfile import NamedTemporaryFile

### Load CSV
def load_csv(input_csv):
    df = pd.read_csv(input_csv)
    return df

### Query
def generate_response(df, input_query):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo',
                     openai_api_key=st.secrets["openai_key"],
                     streaming=True)
    # # Create Pandas DataFrame Agent
    # agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)

    agent = create_csv_agent(llm, df)

    # Perform Query using the Agent
    response = agent.run(input_query)
    response = response.replace("dataframe", "dataset")
    return response 

###
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

###
st.set_page_config(layout="wide")
st.title("Survey GPT")
st.write("This version uses langchain agents")


openai.api_key = st.secrets["openai_key"]


with st.sidebar:
    uploaded_file = st.file_uploader('Select your .csv file', type=['csv'])
    if uploaded_file is not None:
        df = load_csv(uploaded_file)
        with st.expander("Preview Dataset"):
            st.write(df.head(5))

if uploaded_file is None:
    st.markdown("### Please upload your dataset on the left")

if uploaded_file is not None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Say something")

    if prompt := st.chat_input("What do you want to find out?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Please wait..."):
                with NamedTemporaryFile() as f:
                    f.write(uploaded_file.getvalue())
                    full_response = generate_response(f.name, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # if query is not None:
    #    generate_response(df, query)

# query = load_csv("Query")

# if query != "":
#     st.spinner("Please wait...")
#     reply = agent.run(query)
#     st.info(reply)