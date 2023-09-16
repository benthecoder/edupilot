import streamlit as st
from utils import openai_call

st.title("Transcript Summarizer")

with st.form("my_form"):
    transcript_file = st.selectbox(
        "Select a transcript file", options=st.session_state.transcripts
    )

    with open("transcripts/" + transcript_file, "r") as f:
        lecture = f.read()

    # Submit button
    submitted = st.form_submit_button("Summarize Transcript")
    if submitted:
        st.session_state.messages.clear()

        # Create the prompt here
        prompt = f"""
        Consider this lecture transcript:
        {lecture}

        Write a high-quality summary of the lecture in your own words. Then, create 3-5 reflective questions that help students engage with the content at a deeper level.
        """

        st.session_state.messages.extend(
            [
                {
                    "role": "system",
                    "content": "Your task is to summarize this lecture and generate reflective questions for students.",
                },
                {"role": "user", "content": prompt},
            ]
        )

        message_placeholder = st.empty()
        openai_call(st.session_state.messages, message_placeholder)
