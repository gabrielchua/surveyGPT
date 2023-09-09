import os
import streamlit as st
import pandas as pd
from pandasql import sqldf
import openai

st.title("surveyGPT")

openai.api_type = 'azure'
openai.api_base = 'https://launchpad-assistant-api.launchpad.tech.gov.sg/services/openai/'
openai.api_version = '2023-03-15-preview'
openai.api_key = st.secrets["launchpad_key"]


with st.sidebar:
    uploaded_file = st.file_uploader('Select your .csv file', type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        with st.expander("Preview Dataset"):
            st.write(df.head(5))

        num_rows = df.shape[0]
        num_cols = df.shape[1]
        columns = df.columns
        sample_rows = df.head(5)
        system_message_initial = f"""

        You are given a table called "df" with {num_rows} rows and {num_cols} columns.
        The columns are {columns}.
        This data is from a survey.

        Here is the first five rows of the data: {sample_rows}

        You are a SQL programmer using Python Pandas, must only reply in pandasql code.
        I will ask you questions about this table and you must reply with the SQL code to get that answer.
        Do not include any explanations and begin the reply with code.

        For example: "SELECT ..."

        Only if the dataset cannot answer the question, reply with "Information is not likely found in the dataset".

        """

        system_message_interpretation = f"""

        You are given a table called "df" with {num_rows} rows and {num_cols} columns.
        The columns are {columns}.
        This data is from a survey.

        You will receive a question and the results from a pandas dataframe.

        Based only on the results, answer the question.


        """

########
def ask_dataset(df, query):
    sql_reply = openai.ChatCompletion.create(
                    engine="gpt-35-turbo",
                    messages=[
                            {"role": "system", "content": system_message_initial},
                            {"role": "user", "content": query},
                        ]
                    )
    sql_query = sql_reply["choices"][0]["message"]["content"]
    sql_query = sql_query.replace("\n", " ")
    
    result = sqldf(sql_query)


    query_with_data = f"""
    query: {query}
    dataframe result: {result}
    """

    sql_interpretation = openai.ChatCompletion.create(
                    engine="gpt-35-turbo",
                    messages=[
                            {"role": "system", "content": system_message_interpretation},
                            {"role": "user", "content": query_with_data},
                        ]
                    )

    sql_interpretation = sql_interpretation["choices"][0]["message"]["content"]
    return sql_interpretation

#########
if uploaded_file is not None:

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": f"Thanks for uploading your dataset (N={num_rows}). How may I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Say something")

    if query := st.chat_input("What do you want to find out?"):
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Please wait..."):
                full_response = ask_dataset(df, query)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})