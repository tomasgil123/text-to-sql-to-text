import streamlit as st

st.title('How does it work under the hood?')
intro = """
    Under the hood the app uses gpt-3.5-turbo. When the users types a question, the app asks the model
    to come up with a sql script that answers the user question, given the database schema and other information we shared in the prompt.
    The app then executes the sql script using a library called SQLAlchemy, pass the result back to the model and asks it to
    output a final answer using those results. Thats why the app is called text to SQL to text.
"""

intro_prompt_first = """
    A prompt example: 
"""

intro_prompt_code = """
    [{"role": "user", "content": "You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.\\n
    Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.\\n
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (\\") to denote them as delimited identifiers.\\nPay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.\\n
    Pay attention to use CURRENT_DATE function to get the current date, if the question involves \\"today\\".\\n\\n
    Use the following format:\\n\\nQuestion: Question here\\nSQLQuery: SQL Query to run\\nSQLResult: Result of the SQLQuery\\nAnswer: Final answer here\\n\\nOnly use the following tables:\\n\\n
    CREATE TABLE lms.courses (\\n\\tid VARCHAR(255) NOT NULL, \\n\\ttitle VARCHAR(255) NOT NULL, \\n\\tdescription TEXT, \\n\\tduration INTEGER, \\n\\tauthor VARCHAR(255), \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tquestionnaire_id INTEGER, \\n\\tresources_id VARCHAR(255), \\n\\tcertificate_id VARCHAR(255), \\n\\tCONSTRAINT courses_pkey PRIMARY KEY (id)\\n)\\n\\n/*\\n3 
    rows from courses table:\\nid\\ttitle\\tdescription\\tduration\\tauthor\\tcreated_at\\tupdated_at\\tquestionnaire_id\\tresources_id\\tcertificate_id\\n1m7yPrhvn7pIPtKraCv8NdVkQL2TvJV5Z\\tDocker and Kubernetes The Complete Guide\\tNone\\tNone\\tNone\\t2023-05-12 17:49:57.005020\\t2023-05-12 17:49:57.005020\\tNone\\tNone\\tNone\\n1UWxY2gu0ku_TAIeCAJeERBd8TyWsGfVa\\tAWS Fundamentals for Beginner\\tNone\\tNone\\tNone\\t2023-05-03 10:11:36.054128\\t2023-05-03 10:11:36.054128\\t3\\tNone\\tNone\\n1kFAntT6pf_JD700yZi8KInfvevYd0jBV\\tGoogle Cloud Platform(GCP) Essential Training for Developers\\tNone\\tNone\\tNone\\t2023-05-03 10:11:36.054128\\t2023-05-03 10:11:36.054128\\t5\\tNone\\tNone\\n*/\\n\\n\\n
    CREATE TABLE lms.users (\\n\\tid SERIAL NOT NULL, \\n\\tname VARCHAR(255) NOT NULL, \\n\\temail VARCHAR(255) NOT NULL, \\n\\tgoogle_id VARCHAR(255), \\n\\tpicture_url VARCHAR(255), \\n\\trole VARCHAR(8) NOT NULL, \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, \\n\\tlast_online TIMESTAMP WITHOUT TIME ZONE, \\n\\tmanager_email VARCHAR(255), \\n\\tCONSTRAINT users_pkey PRIMARY KEY (id), \\n\\tCONSTRAINT users_email_key UNIQUE (email), \\n\\tCONSTRAINT users_google_id_key UNIQUE (google_id)\\n)\\n\\n/*\\n3 
    rows from users table:\\nid\\tname\\temail\\tgoogle_id\\tpicture_url\\trole\\tcreated_at\\tupdated_at\\tlast_online\\tmanager_email\\n28\\tRafael Cardenas\\trafael.cardenas@agileengine.com\\tNone\\thttps://lh3.googleusercontent.com/a/AGNmyxYcscCfsDx38zBJxbWrliowHLmu73GwB1tlX9PT=s96-c\\tUSER\\t2023-05-23 21:15:01.806000\\t2023-05-23 21:15:01.806000\\tNone\\tNone\\n29\\tAndrey Trubin\\tandrey.trubin@agileengine.com\\tNone\\thttps://lh3.googleusercontent.com/a/AAcHTtdhMa_u58yWqxcK4UTHsdhwzji70-9SVT1hhpRp=s96-c\\tUSER\\t2023-06-01 13:57:38.709000\\t2023-06-01 13:57:38.709000\\tNone\\tNone\\n4\\tDmytro Piddubnyi\\tdmytro.piddubnyi@agileengine.com\\tNone\\thttps://lh3.googleusercontent.com/a/AGNmyxbZYAB_HPxS83HY-wZnF1cXPQxZqEGOc8-tGaM4=s96-c\\tUSER\\t2023-05-01 11:59:33.579000\\t2023-05-01 11:59:33.579000\\tNone\\tNone\\n*/\\n\\n\\n
    CREATE TABLE lms.chapters (\\n\\tid VARCHAR(255) NOT NULL, \\n\\tcourse_id VARCHAR(255), \\n\\ttitle VARCHAR(255), \\n\\tduration INTEGER, \\n\\tposition INTEGER, \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tCONSTRAINT chapters_pkey PRIMARY KEY (id), \\n\\tCONSTRAINT chapters_course_id_fkey FOREIGN KEY(course_id) REFERENCES lms.courses (id)\\n)\\n\\n/*\\n3 
    rows from chapters table:\\nid\\tcourse_id\\ttitle\\tduration\\tposition\\tcreated_at\\tupdated_at\\n1O8sUwv6rkToNbxVAUnSrF0pff1Nrc1Il\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\t1. Introduction\\tNone\\t1\\t2023-04-26 10:55:29.539017\\t2023-04-26 10:55:29.539017\\n1Nn6tFwQWOGgH0fCmH5J46hMHgidhB137\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\t2. Worksheet Operations, Cells, Ranges and Tables\\tNone\\t2\\t2023-04-26 10:55:29.539017\\t2023-04-26 10:55:29.539017\\n192AbgpDPfhGCPNX5I8taZVt_NOLdNi4u\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\t3. Formats & Conditional Formatting\\tNone\\t3\\t2023-04-26 10:55:29.539017\\t2023-04-26 10:55:29.539017\\n*/\\n\\n\\n
    CREATE TABLE lms.user_courses (\\n\\tid SERIAL NOT NULL, \\n\\tuser_id INTEGER NOT NULL, \\n\\tcourse_id VARCHAR NOT NULL, \\n\\tassigned BOOLEAN NOT NULL, \\n\\tuser_id_admin INTEGER, \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), \\n\\tCONSTRAINT user_courses_pkey PRIMARY KEY (id), \\n\\tCONSTRAINT user_courses_course_id_fkey FOREIGN KEY(course_id) REFERENCES lms.courses (id), \\n\\tCONSTRAINT user_courses_user_id_admin_fkey FOREIGN KEY(user_id_admin) REFERENCES lms.users (id), \\n\\tCONSTRAINT user_courses_user_id_fkey FOREIGN KEY(user_id) REFERENCES lms.users (id)\\n)\\n\\n/*\\n3 
    rows from user_courses table:\\nid\\tuser_id\\tcourse_id\\tassigned\\tuser_id_admin\\tcreated_at\\tupdated_at\\n274\\t6\\t1SkdvS93uhwggKsBqoTT7TxTik-t-nUCB\\tTrue\\tNone\\t2023-06-01 19:27:57.716000\\t2023-06-01 19:27:57.716000\\n275\\t6\\t1Y8FQfOWmzHEN_H9WkuT8dXvygjBiPTsu\\tTrue\\tNone\\t2023-06-01 19:27:57.726000\\t2023-06-01 19:27:57.726000\\n276\\t6\\t1YKKBqI4c0godA0TFWIRb7-Oazy9gML9g\\tTrue\\tNone\\t2023-06-01 19:27:57.733000\\t2023-06-01 19:27:57.733000\\n*/\\n\\n\\n
    CREATE TABLE lms.videos (\\n\\tid VARCHAR(255) NOT NULL, \\n\\tchapter_id VARCHAR(255), \\n\\ttitle VARCHAR(255), \\n\\tdescription TEXT, \\n\\tduration INTEGER, \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE, \\n\\tCONSTRAINT videos_pkey PRIMARY KEY (id), \\n\\tCONSTRAINT videos_chapter_id_fkey FOREIGN KEY(chapter_id) REFERENCES lms.chapters (id)\\n)\\n\\n/*\\n3 
    rows from videos table:\\nid\\tchapter_id\\ttitle\\tdescription\\tduration\\tcreated_at\\tupdated_at\\n1uxPoA6sT5hXVcp-NWMkXDOOuejpvGyi3\\t1O8sUwv6rkToNbxVAUnSrF0pff1Nrc1Il\\t1. Introduction\\tNone\\tNone\\t2023-04-26 10:59:03.208569\\t2023-04-26 10:59:03.208569\\n1-BbZxmfId6hjUaYxArYxJdVqSPf3Udve\\t1O8sUwv6rkToNbxVAUnSrF0pff1Nrc1Il\\t2. Building Blocks\\tNone\\tNone\\t2023-04-26 10:59:03.208569\\t2023-04-26 10:59:03.208569\\n1EhxXcO-VBuFrL04bXS4mg721DyEbKQO_\\t1O8sUwv6rkToNbxVAUnSrF0pff1Nrc1Il\\t3. Toolbar\\tNone\\tNone\\t2023-04-26 10:59:03.208569\\t2023-04-26 10:59:03.208569\\n*/\\n\\n\\n
    CREATE TABLE lms.user_video_progress (\\n\\tid SERIAL NOT NULL, \\n\\tuser_id INTEGER NOT NULL, \\n\\tvideo_id VARCHAR(255) NOT NULL, \\n\\tcompleted BOOLEAN DEFAULT true, \\n\\tcreated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), \\n\\tupdated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), \\n\\tcourse_id VARCHAR(255) NOT NULL, \\n\\tCONSTRAINT user_video_progress_pkey PRIMARY KEY (id), \\n\\tCONSTRAINT user_video_progress_user_id_fkey FOREIGN KEY(user_id) REFERENCES lms.users (id), \\n\\tCONSTRAINT user_video_progress_video_id_fkey FOREIGN KEY(video_id) REFERENCES lms.videos (id), \\n\\tCONSTRAINT user_video_progress_user_id_video_id_key UNIQUE (user_id, video_id)\\n)\\n\\n/*\\n
    3 rows from user_video_progress table:\\nid\\tuser_id\\tvideo_id\\tcompleted\\tcreated_at\\tupdated_at\\tcourse_id\\n154\\t3\\t1Y5oBJdiawVhp6HYlbNoU_XxcVmFQR6AE\\tTrue\\t2023-05-08 22:02:53.294000\\t2023-05-08 22:02:53.294000\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\n155\\t3\\t1BET7mI22tGp9oXdvnKcDkMIOiKQNqQEu\\tTrue\\t2023-05-08 22:02:53.860000\\t2023-05-08 22:02:53.860000\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\n167\\t3\\t17MrbKd1bFimRLo0h0AFIU_SBVHKFPVxl\\tTrue\\t2023-05-08 22:03:07.388000\\t2023-05-08 22:03:07.388000\\t1biDY0recPVPXGPd2Vd28jDfl8BZO5cc-\\n*/\\n\\n
    Question: How many courses do we have?}]
"""

intro_prompt_second = """
    Notice the prompt includes info about every table in the database and also the first three rows of each table, plus the user query.
"""

intro_markdown = f"""
    <p style='font-size: 16px;'>{intro}</p>
"""

st.markdown(intro_markdown, unsafe_allow_html=True)

intro_prompt_first_markdown = f"""
    <p style='font-size: 16px;'>{intro_prompt_first}</p>
"""
intro_prompt_second_markdown = f"""
    <p style='font-size: 16px;'>{intro_prompt_second}</p>
"""

st.markdown(intro_prompt_first_markdown, unsafe_allow_html=True)
st.code(intro_prompt_code, language='python')
st.markdown(intro_prompt_second_markdown, unsafe_allow_html=True)




