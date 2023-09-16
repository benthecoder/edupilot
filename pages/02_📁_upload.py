import streamlit as st
from pathlib import Path
import os


def main():
    st.title("Upload your lectures")

    # Get the lecture title
    lecture_title = st.text_input("Enter the title for the lecture")

    # Form for uploading the transcript
    file_uploaded = st.file_uploader(
        "Upload your class transcription file", type=["txt"]
    )

    # Creating a folder named 'transcripts'
    folder_path = Path.cwd() / "transcripts"
    folder_path.mkdir(parents=True, exist_ok=True)

    # When the 'Upload' button is clicked
    if st.button("Upload"):
        try:
            # Checking if the lecture title and file are provided correctly.
            if not lecture_title:
                st.error("Lecture title is missing. It's a required field.")
                return

            if not file_uploaded:
                st.error(
                    "No file provided. Please, provide a class transcription file."
                )
                return

            # Upload the file with lecture_title.txt format
            with open(os.path.join(folder_path, lecture_title + ".txt"), "wb") as f:
                f.write(file_uploaded.getbuffer())

            # The file upload was a success
            st.success(f"Success! The file {lecture_title}.txt has been uploaded")
        except Exception as e:
            # The file upload failed
            st.error(f"An error has occurred: {e}")


if __name__ == "__main__":
    main()
