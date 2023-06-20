import streamlit as st

st.title('Future challenges')
intro_llms = """
    LLMs, like gpt-3.5-turbo, have been trained on a large corpus of public text. This allows them to
    answer a wide range of questions about public topics. However, they are not trained on private data, like the schema and tables
    that make up a database. So they can't help us coming up with SQL queries to answer questions about private data.
    There is two ways to make the LLM model "aware" of our private data. The first one is to fine-tune the model on our data, which is
    expensive and time consuming (although that might change in the future). The second one is to provide the model with a prompt that
    includes our private data. This is what we are doing here. We are providing the model with a prompt that includes info about our database.
    This technique is called "prompt engineering".
"""

intro_llms_markdown = f"""
    <p style='font-size: 16px;'>{intro_llms}</p>
"""

st.markdown(intro_llms_markdown, unsafe_allow_html=True)

prompt_engineering = """
    One important feature or limitation of LLMs is that the prompt you can pass to them is limited to a certain number of tokens (for example, 4000 tokens
    for gpt-3.5-turbo). Also, the more tokens you include in the prompt the more expensive the request becomes.
    Prompt engineering is a set of techniques to design a prompt in such a way it includes the most relevant information given
    a user query and the token limitation of the model. It is also important "how" you include this information in the prompt. Notice
    in our previous prompt example that each table schema is preceded by a "create table" statement. 
    A study evaluating the Text-to-SQL performance of OpenAI Codex given a variety of different prompting structures,
    found that best performance is achieved when prompting Codex with the CREATE TABLE commands, which include column names, their types, column references, and keys.
    (you can read more about that here: https://arxiv.org/abs/2204.00498)
    In the previous example we are dealing with a relatively small database, so all the information about the database fits in the prompt.
    But that won't be always the case. When the relevant info exceeds the tokens limitations you have to decide which info to include 
    in the prompt. Thats when things like embeddings and vector stores come in handy, which require more time and effort to implement.
    <b>I think the main challenge this type of applications face is how to use embeddings to build up the prompt given the token limitations.</b>
    A library which provides a wide set of tools to create embeddings, store them in a vector store and query that vector store is 
    langchain. You can read more about it here: https://python.langchain.com/docs/modules/data_connection/
"""

prompt_engineering_markdown = f"""
    <p style='font-size: 16px;'>{prompt_engineering}</p>
"""

st.markdown(prompt_engineering_markdown, unsafe_allow_html=True)