import streamlit as st
import whisper
import numpy as np
import sounddevice as sd
import queue
import tempfile
import os
import scipy.io.wavfile as wav
import google.generativeai as genai
import time

# Set page config
st.set_page_config(page_title="Dream Interpretation", page_icon="🌙", layout="wide")

# Apply custom CSS for improved UI
st.markdown("""
    <style>
    /* General styling */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
    }

    /* Background Image */
    .reportview-container {
        background-image: url('https://images.pexels.com/photos/1341279/pexels-photo-1341279.jpeg?auto=compress&cs=tinysrgb&w=auto'); 
        background-size: cover;
        background-position: center;
        padding: 20px;
    }
    /* Header */
    h1 {
        font-size: 2.5rem;
        color: #fff;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }

    /* Subheader */
    h2 {
        color: #e5e5e5;
        font-weight: 600;
        font-size: 1.5rem;
    }

    /* Buttons Styling */
    .stButton button {
        padding: 10px 20px;
        text-transform: uppercase;
        border-radius: 8px;
        font-size: 17px;
        font-weight: 500;
        color: #ffffff80;
        text-shadow: none;
        background: transparent;
        cursor: pointer;
        box-shadow: transparent;
        border: 1px solid #ffffff80;
        transition: 0.5s ease;
        user-select: none;
    }

    .stButton button:hover, .stButton button:focus {
        color: #ffffff;
        background: #008cff;
        border: 1px solid #008cff;
        text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 20px #ffffff;
        box-shadow: 0 0 5px #008cff, 0 0 20px #008cff, 0 0 50px #008cff,0 0 100px #008cff;
    }

    .stButton button:active {
        transform: scale(0.98);
    }

    /* Input Styling */
    .stNumberInput input {
        background-color: #333;
        color: white;
        border: 1px solid #666;
        border-radius: 5px;
        padding: 10px;
    }

    .stNumberInput input:focus {
        border-color: #4CAF50;
    }

    /* Footer Styling */
    footer {
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #bbb;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
        backdrop-filter: blur(5px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Configure Gemini API
if 'GEMINI_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
else:
    st.error("Gemini API key not found in secrets!")

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")

whisper_model = load_whisper_model()

# New Gemini function with improved error handling
def generate_gemini_response(dream_description):
    """Generate interpretation using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        You are a Dream Interpreter. 
        I will provide you with a description of a dream, and your task is to analyze it and provide a detailed interpretation based on psychological, symbolic, and emotional themes. 
        Use known dream analysis frameworks such as Freudian, Jungian, and common cultural interpretations to explain the meaning of the dream. 
        Be sensitive to the emotions expressed in the dream and consider potential real-life influences.
        At last provide the summary.

        Dream: "{dream_description}"
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, something went wrong while interpreting the dream."

# Transcription function for live audio
def transcribe_audio_live(audio_data, fs):
    """Transcribe live audio data using Whisper model"""
    temp_path = tempfile.mktemp(suffix=".wav")
    wav.write(temp_path, fs, audio_data)  # Save the audio data temporarily
    audio = whisper.load_audio(temp_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(whisper_model, mel, options)
    os.remove(temp_path)  # Clean up the temporary file
    return result.text

# Initialize session state for recording text
if 'recorded_text' not in st.session_state:
    st.session_state.recorded_text = None

# ========== Live Recording Section ==========  
st.title("🌙 Dream Analyzer: Decode Your Dreams with AI")

# Audio callback function
q = queue.Queue()
fs = 16000  # Sampling frequency
channels = 1  # Number of channels

def callback(indata, frames, time, status):
    """Callback function for audio input stream"""
    if status:
        print(status)
    q.put(indata.copy())

# Recording controls UI with style
col1, col2 = st.columns([2, 1])  # Adjust column width ratio
with col1:
    duration = st.number_input("Recording Duration (seconds)", min_value=1, max_value=60, value=10, help="Select the recording duration")

with col2:
    st.write("")  # Add some vertical spacing to align with number input
    start_recording = st.button("Start Recording 🎤", use_container_width=True, key="start_button")

if start_recording:
    st.write("Listening... Speak now!")

    # Start recording
    with sd.InputStream(callback=callback, channels=channels, samplerate=fs):
        sd.rec(int(fs * duration), samplerate=fs, channels=channels, dtype=np.int16)
        sd.wait()

    # Process audio data
    audio_data = np.concatenate([q.get() for _ in range(q.qsize())], axis=0)
    
    # Save temporary audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        wav.write(temp_audio.name, fs, audio_data)
        temp_path = temp_audio.name

    # Transcribe and display results
    st.write("Transcribing... ⏳")
    try:
        text = transcribe_audio_live(audio_data, fs)
        st.session_state.recorded_text = text  # Store the text in session state
        st.subheader("Transcribed Text:")
        st.write(text)
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")

# Interpret button and Gemini analysis
if st.session_state.recorded_text:
    if st.button("Interpret My Dream", key="interpret_button"):
        with st.spinner("Analyzing your dream..."):
            gemini_response = generate_gemini_response(st.session_state.recorded_text)
            time.sleep(2)
            st.subheader("🌙 Dream Interpretation Result:")
            st.markdown(gemini_response)

# Add some footer text with branding or additional info
st.markdown("""
    <footer>
        Created with ❤️ by Talha Rauf
    </footer>
    """, unsafe_allow_html=True)



