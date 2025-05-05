"""
Module for processing and concatenating Quran audio files.
"""

import os
from typing import List, Optional
import logging
from pydub import AudioSegment

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def concatenate_audio_files(audio_files: List[str], output_file: str) -> Optional[str]:
    """
    Concatenate multiple audio files into a single file.
    
    Args:
        audio_files: List of paths to audio files to concatenate
        output_file: Path to save the concatenated audio file
        
    Returns:
        Path to the concatenated audio file or None if failed
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if we have files to concatenate
        if not audio_files:
            logger.error("No audio files to concatenate")
            return None
        
        # Load the first audio file
        combined = AudioSegment.from_mp3(audio_files[0])
        logger.info(f"Loaded first audio file: {audio_files[0]}")
        
        # Add the rest of the audio files
        for audio_file in audio_files[1:]:
            try:
                sound = AudioSegment.from_mp3(audio_file)
                combined += sound
                logger.info(f"Added audio file: {audio_file}")
            except Exception as e:
                logger.error(f"Error processing file {audio_file}: {e}")
                # Continue with other files if one fails
        
        # Export the combined audio file
        combined.export(output_file, format="mp3")
        logger.info(f"Successfully created concatenated audio file: {output_file}")
        
        return output_file
    
    except Exception as e:
        logger.error(f"Error concatenating audio files: {e}")
        return None


def generate_output_filename(start_ayah: str, end_ayah: str, surah_name: str) -> str:
    """
    Generate an output filename for the concatenated audio based on the ayah range.
    
    Args:
        start_ayah: Starting ayah reference (format: 'surah:ayah')
        end_ayah: Ending ayah reference (format: 'surah:ayah')
        surah_name: Name of the surah
        
    Returns:
        A formatted filename for the output audio file
    """
    try:
        # Parse the ayah references
        start_parts = start_ayah.split(':')
        end_parts = end_ayah.split(':')
        
        surah_num = start_parts[0].zfill(3)
        start_ayah_num = start_parts[1].zfill(3)
        end_ayah_num = end_parts[1].zfill(3)
        
        # Format the filename
        filename = f"{surah_num}_{surah_name}_{start_ayah_num}-{end_ayah_num}.mp3"
        
        # Remove any special characters that are not suitable for filenames
        filename = "".join(c for c in filename if c.isalnum() or c in ['-', '_', '.'])
        
        return filename
    
    except Exception as e:
        logger.error(f"Error generating output filename: {e}")
        # Fallback to a default filename
        return f"quran_audio_{start_ayah}-{end_ayah}.mp3"