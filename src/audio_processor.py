"""
Module for processing and concatenating Quran audio files.
"""

from typing import List, Optional
import logging
import os
import subprocess
import imageio_ffmpeg

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def concatenate_audio_files(audio_files: List[str], output_file: str) -> Optional[str]:
    """
    Concatenate multiple audio files into a single file using imageio-ffmpeg.
    
    Args:
        audio_files: List of paths to audio files to concatenate
        output_file: Path to save the concatenated audio file
        
    Returns:
        Path to the concatenated audio file or None if failed
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Check if we have files to concatenate
        if not audio_files:
            logger.error("No audio files to concatenate")
            return None
        
        # Create a temporary ffmpeg input list file for concatenation
        list_file_path = os.path.join(output_dir if output_dir else ".", "file_list.txt")
        with open(list_file_path, "w", encoding="utf-8") as f:
            for file in audio_files:
                abs_path = os.path.abspath(file)
                f.write(f"file '{abs_path}'\n")
        
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe, "-y", "-f", "concat", "-safe", "0",
            "-i", list_file_path, "-c", "copy", output_file
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Clean up temporary list file
        if os.path.exists(list_file_path):
            os.remove(list_file_path)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return None
            
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
