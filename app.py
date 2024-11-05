import streamlit as st
from google.cloud import speech
import soundfile as sf
import io

# Initialize Google Cloud Speech client
client = speech.SpeechClient()

def transcribe_audio(audio_file):
    # Read audio file
    data, samplerate = sf.read(audio_file, dtype='int16')
    with io.BytesIO() as wav_io:
        sf.write(wav_io, data, samplerate, format="WAV")
        wav_content = wav_io.getvalue()

    # Configure audio and transcription settings
    audio = speech.RecognitionAudio(content=wav_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=samplerate,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    # Call Google Speech-to-Text API
    response = client.recognize(config=config, audio=audio)

    # Extract and return transcription
    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "
    return transcription.strip()

st.title("Audio File Transcription App")

# Upload audio file
uploaded_file = st.file_uploader("Upload a WAV audio file for transcription", type=["wav"])

if uploaded_file is not None:
    st.write("Transcribing audio...")
    transcription = transcribe_audio(uploaded_file)
    st.subheader("Transcription:")
    st.write(transcription)
