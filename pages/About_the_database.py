import streamlit as st

st.title('About the database')

description = f"""
The given database is a Learning Management System (LMS) database. It contains tables related to courses, users, chapters, user-course associations, videos, and user video progress.

The "courses" table stores information about different courses, including their titles, descriptions, durations, authors, and timestamps for creation and updates.

The "users" table holds user details such as names, emails, Google IDs, profile picture URLs, roles, and timestamps for creation, updates, and last online activity.

The "chapters" table is likely used to organize course content into chapters, with information such as chapter titles, durations, positions, and timestamps for creation and updates.

The "user_courses" table represents the association between users and courses, tracking assigned status and timestamps for creation and updates. It also includes foreign key constraints to ensure referential integrity.

The "videos" table stores information about course videos, including their titles, descriptions, durations, and timestamps for creation and updates. It also has a foreign key referencing the "chapters" table to establish relationships.

Finally, the "user_video_progress" table tracks the progress of users in watching videos, including information such as completion status, timestamps for creation and updates, and the associated course. 
"""

description_markdown = f"""
    <p style='font-size: 16px;'>{description}</p>
"""

st.markdown(description_markdown, unsafe_allow_html=True)

courses_table = """
CREATE TABLE lms.courses (
    id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration INTEGER,
    author VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    questionnaire_id INTEGER,
    resources_id VARCHAR(255),
    certificate_id VARCHAR(255),
    CONSTRAINT courses_pkey PRIMARY KEY (id)
)
"""

users_table = """
CREATE TABLE lms.users (
    id SERIAL NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    google_id VARCHAR(255),
    picture_url VARCHAR(255),
    role VARCHAR(8) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_online TIMESTAMP WITHOUT TIME ZONE,
    manager_email VARCHAR(255),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_google_id_key UNIQUE (google_id)
)
"""
chapters_table = """
CREATE TABLE lms.chapters (
    id VARCHAR(255) NOT NULL,
    course_id VARCHAR(255),
    title VARCHAR(255),
    duration INTEGER,
    position INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT chapters_pkey PRIMARY KEY (id),
    CONSTRAINT chapters_course_id_fkey FOREIGN KEY(course_id) REFERENCES lms.courses (id)
)
"""
user_courses_table = """
CREATE TABLE lms.user_courses (
    id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    course_id VARCHAR NOT NULL,
    assigned BOOLEAN NOT NULL,
    user_id_admin INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    CONSTRAINT user_courses_pkey PRIMARY KEY (id),
    CONSTRAINT user_courses_course_id_fkey FOREIGN KEY(course_id) REFERENCES lms.courses (id),
    CONSTRAINT user_courses_user_id_admin_fkey FOREIGN KEY(user_id_admin) REFERENCES lms.users (id),
    CONSTRAINT user_courses_user_id_fkey FOREIGN KEY(user_id) REFERENCES lms.users (id)
)
"""

videos_table = """
CREATE TABLE lms.videos (
    id VARCHAR(255) NOT NULL,
    chapter_id VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    duration INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT videos_pkey PRIMARY KEY (id),
    CONSTRAINT videos_chapter_id_fkey FOREIGN KEY(chapter_id) REFERENCES lms.chapters (id)
)
"""
user_video_progress_table = """
CREATE TABLE lms.user_video_progress (
    id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    video_id VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    course_id VARCHAR(255) NOT NULL,
    CONSTRAINT user_video_progress_pkey PRIMARY KEY (id),
    CONSTRAINT user_video_progress_user_id_fkey FOREIGN KEY(user_id) REFERENCES lms.users (id),
    CONSTRAINT user_video_progress_video_id_fkey FOREIGN KEY(video_id) REFERENCES lms.videos (id),
    CONSTRAINT user_video_progress_user_id_video_id_key UNIQUE (user_id, video_id)
)
"""
st.code(courses_table, language='sql')
st.code(users_table, language='sql')
st.code(chapters_table, language='sql')
st.code(user_courses_table, language='sql')
st.code(videos_table, language='sql')
st.code(user_video_progress_table, language='sql')


