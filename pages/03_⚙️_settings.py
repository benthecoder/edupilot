import streamlit as st


sample_title = "The Early Middle Ages, 284–1000"
sample_desc = "Major developments in the political, social, and religious history of Western Europe from the accession of Diocletian to the feudal transformation. Topics include the conversion of Europe to Christianity, the fall of the Roman Empire, the rise of Islam and the Arabs, the “Dark Ages,” Charlemagne and the Carolingian renaissance, and the Viking and Hungarian invasions."

# create two textbox show the current value of the session state if it exists
title = st.text_input("Class Title", value=sample_title)
desc = st.text_area("Class Description", value=sample_desc, height=200)

if st.button("Save"):
    st.session_state.title = title
    st.session_state.description = desc

    st.success("Class info saved!")
