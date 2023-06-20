import streamlit as st

st.title('Current app limitations')

limitations = f"""

- The app doesn't have "memory". Every query the user makes is a distinct conversation with the LLM model. In other words,
the LLM doesn't remember about previous interactions, like the chat gpt application does.

- Not much time has been spent on optimizing the prompt. I relied on a library called langchain to provide some basic
optimizations.

- The feedback to the user is not very good. The application is slow and the user might not know when something is loading or not. Also,
errors are displayed in a very raw way.

- Queries, answers and charts aren't being stored anywhere.

- I didn't try a lot of queries, very complex queries might not work.
"""

limitations_markdown = f"""
    <p style='font-size: 16px;'>{limitations}</p>
"""

st.markdown(limitations_markdown, unsafe_allow_html=True)