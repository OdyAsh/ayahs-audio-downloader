"""
Ayahs Audio Downloader - A Streamlit application for downloading and concatenating Quran audio files.
"""

import os
import time
import re
import streamlit as st
import base64
from src.audio_downloader import (
    get_available_reciters,
    download_ayah_range,
    get_surah_name,
    parse_ayah_reference,
    get_reciter_id_by_name
)
from src.audio_processor import concatenate_audio_files, generate_output_filename

# Set page configuration
st.set_page_config(
    page_title="Ayahs Audio Downloader",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Define paths
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Create directories if they don't exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to validate ayah reference format
def validate_ayah_format(ayah_ref):
    """Validate the format of an ayah reference (e.g., '2:5')"""
    if not ayah_ref:
        return False
    pattern = r'^\d+:\d+$'
    return bool(re.match(pattern, ayah_ref))

# Function to get a download link for a file
def get_download_link(file_path, link_text):
    """Generate a download link for a file"""
    with open(file_path, "rb") as file:
        contents = file.read()
    b64 = base64.b64encode(contents).decode()
    filename = os.path.basename(file_path)
    
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Main application
def main():
    st.title("Quran Ayahs Audio Downloader")
    st.markdown("""
    Download and concatenate audio recitations of Quran verses (ayahs) based on a specified range.
    """)
    
    # Initialize session state for tracking process status
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'output_file' not in st.session_state:
        st.session_state.output_file = None

    # Get available reciters
    reciters = get_available_reciters()
    reciter_names = list(reciters.values())
    
    # Input for ayah range
    st.subheader("Select Ayah Range")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_ayah = st.text_input(
            "Starting Ayah (format: surah:ayah)",
            value="1:1",
            help="Enter the starting ayah reference, e.g., '2:1' for Surah Al-Baqarah, Ayah 1"
        )
    
    with col2:
        end_ayah = st.text_input(
            "Ending Ayah (format: surah:ayah)",
            value="1:7",
            help="Enter the ending ayah reference, e.g., '2:7' for Surah Al-Baqarah, Ayah 7"
        )
    
    # Select reciter
    st.subheader("Select Reciter")
    reciter = st.selectbox(
        "Choose a reciter",
        reciter_names,
        index=0,  # Default to Mishary Rashid Al Afasy
        help="Select a reciter for the audio files"
    )
    
    # Process button
    process_btn = st.button("Get Audio File")
    
    # Display a message if inputs are invalid
    if not validate_ayah_format(start_ayah) or not validate_ayah_format(end_ayah):
        st.error("Please enter ayah references in the correct format (e.g., '2:5')")
    
    # Process the request
    if process_btn and validate_ayah_format(start_ayah) and validate_ayah_format(end_ayah):
        try:
            st.session_state.processing = True
            
            # Show progress message
            with st.spinner("Downloading and processing audio files..."):
                # Get reciter ID
                reciter_id = get_reciter_id_by_name(reciter)
                
                # Parse the starting ayah to get surah number
                start_surah, _ = parse_ayah_reference(start_ayah)
                
                # Get surah name for the output filename
                surah_name = get_surah_name(start_surah)
                
                # Download the audio files
                audio_files = download_ayah_range(start_ayah, end_ayah, reciter_id, TEMP_DIR)
                
                if audio_files:
                    # Generate output filename
                    output_filename = generate_output_filename(start_ayah, end_ayah, surah_name)
                    output_file_path = os.path.join(OUTPUT_DIR, output_filename)
                    
                    # Concatenate the audio files
                    result = concatenate_audio_files(audio_files, output_file_path)
                    
                    if result:
                        st.session_state.output_file = output_file_path
                        st.success(f"Successfully processed {len(audio_files)} ayahs!")
                    else:
                        st.error("Error concatenating audio files. Please try again.")
                else:
                    st.error("No audio files could be downloaded. Please check your inputs and try again.")
            
            st.session_state.processing = False
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.processing = False
    
    # Display download link if output file is ready
    if st.session_state.output_file and os.path.exists(st.session_state.output_file):
        st.subheader("Download")
        st.markdown(get_download_link(st.session_state.output_file, "Download Audio File"), unsafe_allow_html=True)
        
        # Add option to play the audio directly
        st.subheader("Listen")
        audio_file = open(st.session_state.output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

if __name__ == "__main__":
    main()