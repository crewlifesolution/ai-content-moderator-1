#Creating the actual app, for this we have to import some libraries 
#Importing all the libraries 

import streamlit as st
from pytube import YouTube
from utilities import get_yt, transcribe_yt


#Creating the title of the app 
st.markdown('Content Moderator for Gaming Videos')
st.title('Check the suitability of videos for your childen')
st.warning('Awaiting URL input in the sidebar')

#Creating the sidebar for the app 
st.sidebar.header('Input parameter')

with st.sidebar.form(key='my_form'):
    URL = st.text_input("Enter the URL for the Youtube video or shorts:")
    submit_button = st.form_submit_button(label='Go')

#Creating the main condition for the app
if submit_button:
    get_yt(URL)
    transcribe_yt()

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label = "Download Zip",
            data = zip_download,
            file_name = "transcription.zip",
            mime = "application/zip"
        )
    
    with st.sidebar.expander('Refer to the example URL'):
        st.code('https://www.youtube.com/watch?v=jk6thMe6Vq8')
        







    
