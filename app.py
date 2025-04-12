import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

GOOGLE_API_KEY = "AIzaSyAYARC3hUao1zF21z7z6TgGwiS9rQ1zpZM"  

# default prompt 
default_prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

# function that extract notes from youtube video url
def extract_transcript_details(youtube_video_url, selected_language='en'):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        
        transcript_text = ""
        for item in transcript_data:
            transcript_text += " " + item["text"]
        
        return transcript_text
    
    except Exception as e:
        st.error(f"An error occurred while fetching the transcript: {str(e)}")
        return None

def generate_gemini_content(transcript_text, user_prompt):
    try:

        genai.configure(api_key=GOOGLE_API_KEY)  

        model_name = "models/gemini-1.5-flash"

    # loading the model
        model = genai.GenerativeModel(model_name)

        prompt = f"{user_prompt}\n\n{transcript_text}"

    # generating content
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        st.error(f"An error occurred while generating content: {str(e)}")
        return None

# streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# select language 
selected_language = st.selectbox("Select Transcript Language", ["en", "hi", "auto"])

# change prompt if you want to
user_prompt = st.text_area("Enter Custom Prompt", default_prompt)

#thumbnail of youtube video
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# generate button
if st.button("Get Detailed Notes"):
    with st.spinner("Fetching transcript and generating notes..."):
        transcript_text = extract_transcript_details(youtube_link, selected_language)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, user_prompt)
            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)