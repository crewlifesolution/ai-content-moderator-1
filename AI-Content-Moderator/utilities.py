#Creating the import libraries 
import streamlit as st 
import os 
from time import sleep 
import requests 
from pytube import YouTube 
from zipfile import ZipFile 

#Creating the status bar 
bar = st.progress(0)

#Taking the API from assembly AI API 
api_key = st.secrets["general"]["api_key"]


#Retrieving audio file from Youtube video 
#So you are transcribing speech to text here 
def get_yt(inputURL):
    video = YouTube(inputURL)
    yt = video.streams.get_audio_only()
    yt.download()

    st.info('2. Audio file has been taken from the uploaded YouTube video')
    bar.progress(10)

#3. Uploading the audio file to assemblyAPI 
#Converting the audio file to text using assembly API
def transcribe_yt():
    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            #print(mp4_file)

    filename = mp4_file
    bar.progress(20)

    #Creating the function to read the file 
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data = read_file(filename))
    audio_url = response.json()['upload_url']
    st.info('3. Your Youtube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    #Now transcribing the audio file 
    #Specifying the endpoint 
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
        "audio_url": audio_url,
        "content_safety": True
    }

    headers = {
        "authorization": api_key,
        "content_type": "application/json"

    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    st.info('4. Transcribing your uploaded audio file')
    bar.progress(40)

    #Extracting the transcript ID 
    transcript_id = transcript_input_response.json()["id"]
    st.info("5. Extracting the transcript ID of your file")
    bar.progress(50)

    #Retreiving the transcription results 
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    st.info('6. Retrieving the transcription results')
    bar.progress(60)

    #Checking if the transcription is complete or not 
    st.warning('Transcription is processing...')
    while transcript_output_response.json()['status']!= 'completed':
        sleep(1)
        transcript_output_response = requests.get(endpoint, headers = headers)

    bar.progress(100)

    #Printing the entire transciption text
    st.header('Output')

    with st.expander('Show Text'):
        st.success(transcript_output_response.json()["text"])

    
    #Saving the entire transcribed text to a file
    #Save as a txt file 
    yt_txt = open('yt.txt', 'w')
    yt_txt.write(transcript_output_response.json()["text"])
    yt_txt.close()

    #Write JSON to the app to be displayed 
    with st.expander('Show full results'):
        st.write(transcript_output_response.json())

    
    #Write the content_safety_labels
    with st.expander('Show content_safety_labels'):
        st.write(transcript_output_response.json()["content_safety_labels"])

    with st.expander('Summary of safety labels'):
        st.write(transcript_output_response.json()["content_safety_labels"]["summary"])
    

    #Saving as a SRT (Sub rip text) file 
    srt_endpoint = endpoint + "/srt"
    srt_response = requests.get(srt_endpoint, headers=headers)
    with open("yt.srt", "w") as _file:
        _file.write(srt_response.text)
    
    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('yt.txt')
    zip_file.write('yt.srt')
    zip_file.close()


    #Deleting all the processed files 
    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            os.remove(file)
        if file.endswith(".txt"):
            os.remove(file)
        if file.endswith(".srt"):
            os.remove(file)



