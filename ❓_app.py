import streamlit as st
import os
from utils import openai_call, generate_word_document


# Check and initialize Session States
if "title" not in st.session_state:
    st.session_state.title = ""

if "description" not in st.session_state:
    st.session_state.description = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "transcripts" not in st.session_state:
    # load all the transcripts from transcripts folder
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
            value=1,
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
            Based on the transcript given {lecture}, generate {num_questions} insightful, high-level and thought-provoking questions equivalent to an Ivy league standard like Yale. 

            Ensure the questions require deep consideration of the lecture content and are not easily answerable without a clear understanding of the lecture. 

            Instructions by the professor that you must follow: {instructions}

            Question format:
            If it's a multiple choice question, the answer and grading rubric should be just the right answer.

            If it's a short answer question, the answer and grading rubric should be a sample answer, and have key points.

            Questions:
            --------------
            Question {{n}} [n points]: {{question_text}} 

            for multiple choice, be sure to have new lines, like
            A) {{answer_a}} \n
            B) {{answer_b}} \n
            C) {{answer_c}}
            ...

            Answers:
            --------------
            Question {{n}}: {{answer_text}} \n

            Grading Rubric:
            ---------------
            Question {{n}}:
            - Key Point 1: {{key_point_1}} (n points)
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
