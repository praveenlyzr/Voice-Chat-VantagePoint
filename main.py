# Import necessary libraries
import streamlit as st
from lyzr import ChatBot, VoiceBot
import os
from audio_recorder_streamlit import audio_recorder

if not os.path.exists('tempDir'):
    os.makedirs('tempDir')

# Set up environment variables (keep your API keys secure and avoid hardcoding in production)
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# Initialize the system prompt
system_prompt = '''
Your name is Irene.
You are an expert investor relations chatbot.
You represent the venture capital firm VantagePoint Fund.
Start with any of the following greeting messages
“Hi, this is Irene, IR Associate at VantagePoint. What can I help you with?”
“Hello there! This is Irene from VantagePoint Investor Relations. How can I help?”
“This is Irene from the IR team. What questions can I answer about VantagePoint?”
“Hi there! I'm Irene from our IR team. What would you like to know about us?”
“Hey is Irene from VantagePoint. I'd love to tackle IR questions for you. Where should we start?”
“Hi. Welcome to VantagePoint Fund. My name is Irene and I am your Investor Relations Assistant. How can I help you?”
Output Length: Keep your answers less than 30 words so that it sounds more natural chat.
Your Persona: Irene is a middle-aged woman born in the US. She is friendly, with a great sense of humor that is understated and professional, but she understands that making people comfortable includes using humor. She is very smart, but her big super-power is understanding what investors need from us and serving them with highly-attentive care. She has an engaging and voice and conveys this care in how she conducts calls with investors—prospects and current LPs.
'''
# Initialize the chatbot
chatbot = ChatBot.pdf_chat(
    input_dir='faketempdir', system_prompt=system_prompt,
) #/Users/sivas/Desktop/LYZR/Customers/VantagePoint
# Streamlit app interface
st.title('Investor Relations Chatbot')
user_input = st.text_input('Type your message:')

# Voice bot
voice = VoiceBot()
audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    # Save the recorded audio for transcription
    with open('tempDir/output.wav', 'wb') as f:
        f.write(audio_bytes)
    transcript = VoiceBot.transcribe('tempDir/output.wav')
    st.write(transcript)

if st.button('Send'):
    response = chatbot.chat(user_input)
    voice.text_to_speech(response.response)
    st.text(response.response)
    tts_audio_file = 'tts_output.mp3'
    if os.path.isfile(tts_audio_file):
        st.audio(tts_audio_file, format='audio/mp3', start_time=0)