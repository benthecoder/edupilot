import streamlit as st
import os
from utils import openai_call, generate_word_document


if "title" not in st.session_state:
    st.session_state.title = ""

if "description" not in st.session_state:
    st.session_state.description = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "transcripts" not in st.session_state:
    st.session_state.transcripts = [
        files for files in os.listdir("transcripts") if files.endswith(".txt")
    ]


def main():
    st.set_page_config(
        page_title="EdAI",
        page_icon="🏫",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "This application assists in creating high-value assignments.",
        },
    )

    st.title("Welcome to EdAI")

    # If class information is not set, display warning
    if st.session_state.title == "":
        st.warning(
            "Please navigate to the settings page to input your class information."
        )
        st.stop()

    full_response = ""
    with st.form("my_form"):
        st.write(f"Assignments for {st.session_state.title}")

        transcript_file = st.selectbox("Select a lecture file", options=st.session_state.transcripts)

        with open("transcripts/" + transcript_file, "r") as f:
            lecture = f.read()

        # Number of questions input field
        num_questions = st.number_input(
            "Number of questions",
            min_value=1,
            max_value=10,
            value=2,
            help="Enter the number of questions contained in the assignment",
        )

        # More information input field
        instructions = st.text_input(
            "Instructions for assignment",
            help="Add more details about the assignment here. For example, format, important topics, etc.",
        )

        # Submit button
        submitted = st.form_submit_button("Generate Assignment")
        if submitted:
            del st.session_state.messages[:]

            prompt = f"""
            Consider this information:
            Class title: {st.session_state.title}
            Class description: {st.session_state.description}
            
            Transcript:
            {lecture}

            Your task is to generate {num_questions} insightful, high-level and thought-provoking questions equivalent to an Ivy league standard like Yale. You're provided instructions by the professor that you must follow: {instructions}.

            Ensure the questions require deep consideration of the lecture content and are not easily answerable without a clear understanding of the lecture. 

            Below is the format for the questions, answers, and grading rubric:

            Make sure you separate each question and answer on a new line, I dont' want to see information in one paragraph

            Questions:
            --------------
            Question {{n}} [n points]: {{question_text}} 

            for multiple choice questions, make sure each choice is on a new line, like below

            A) {{answer_a}}

            B) {{answer_b}}

            C) {{answer_c}}
            
            D) {{answer_d}}

            Answers:
            --------------
            Question {{n}}: {{answer_text}}


            Grading Rubric:
            ---------------
            Question {{n}}:
            - Key Point {{n}}: {{key_point_1}} (n points)
            ...
            """

            st.session_state.messages.extend(
                [
                    {
                        "role": "system",
                        "content": "Your task is to assist in creating meaningful, high-value assignments for university professors.",
                    },
                    {"role": "user", "content": prompt},
                ]
            )

            message_placeholder = st.empty()
            full_response = openai_call(st.session_state.messages, message_placeholder)

            #st.session_state.messages.extend({"role": "assistant", "content": full_response})

    if full_response != "":
        doc_file = generate_word_document(full_response)
        st.download_button(
            label="Download Assignment",
            data=doc_file,
            file_name='assignment.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )

if __name__ == "__main__":
    main()
