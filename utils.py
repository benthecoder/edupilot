import streamlit as st
import openai
import docx
from docx.shared import Pt
from io import BytesIO

GPT_MODEL = "gpt-4"
openai.api_key = st.secrets["OPENAI_API_KEY"]


def openai_call(message, message_placeholder, model=GPT_MODEL, temperature=0.2):
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=model,
        messages=[{"role": m["role"], "content": m["content"]} for m in message],
        temperature=temperature,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.write(full_response + "|")

    return full_response


def generate_word_document(content):
    # Create a new Document
    doc = docx.Document()

    # Format and add the content to the Document
    styles = doc.styles
    style = styles["Normal"]
    font = style.font
    font.name = "Arial"
    font.size = Pt(12)

    for line in content.split("\n"):
        doc.add_paragraph(line)

    # Save the Document in BytesIO object
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return f
