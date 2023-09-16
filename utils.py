import streamlit as st
import openai

GPT_MODEL = "gpt-4"
openai.api_key = st.secrets["OPENAI_API_KEY"]


def openai_call(message, message_placeholder, model=GPT_MODEL, temperature=0.2):
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        temperature=temperature,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.write(full_response + "|")

    st.session_state.messages.extend({"role": "assistant", "content": full_response})
