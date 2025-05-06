"""
Module for downloading Quran audio files from the Quran API.
"""

import os
import json
import requests
from typing import List, Dict, Tuple, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base URL for the Quran API
API_BASE_URL = "https://quranapi.pages.dev/api"
AUDIO_BASE_URL = "https://the-quran-project.github.io/Quran-Audio/Data"


def parse_ayah_reference(ayah_ref: str) -> Tuple[int, int]:
    """
    Parse an ayah reference like '2:5' to get surah number and ayah number.
    
    Args:
        ayah_ref: String in the format 'surah_number:ayah_number'
        
    Returns:
        Tuple of (surah_number, ayah_number)
    """
    try:
        surah_num, ayah_num = map(int, ayah_ref.split(':'))
        return surah_num, ayah_num
    except Exception as e:
        logger.error(f"Error parsing ayah reference: {e}")
        raise ValueError(f"Invalid ayah reference format: {ayah_ref}. Expected format: 'surah:ayah', e.g., '2:5'")


def get_surah_name(surah_num: int) -> str:
    """
    Get the surah name based on its number.
    
    Args:
        surah_num: The surah number
        
    Returns:
        The name of the surah
    """
    try:
        url = f"{API_BASE_URL}/{surah_num}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('surahName', f"Surah{surah_num}")
    except Exception as e:
        logger.error(f"Error fetching surah name: {e}")
        return f"Surah{surah_num}"


def get_available_reciters() -> Dict[str, str]:
    """
    Get a list of available reciters from the API.
    
    Returns:
        Dictionary mapping reciter IDs to reciter names
    """
    try:
        url = f"{API_BASE_URL}/reciters.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching reciters: {e}")
        # Default reciters based on API documentation
        return {
            "1": "Mishary Rashid Al Afasy",
            "2": "Abu Bakr Al Shatri",
            "3": "Nasser Al Qatami",
            "4": "Yasser Al Dosari",
            "5": "Hani Ar Rifai"
        }


def download_ayah_audio(surah_num: int, ayah_num: int, reciter_id: str, output_dir: str) -> Optional[str]:
    """
    Download audio for a specific ayah from a specific reciter.
    
    Args:
        surah_num: The surah number
        ayah_num: The ayah number
        reciter_id: The reciter ID
        output_dir: Directory to save the downloaded audio
        
    Returns:
        Path to the downloaded audio file or None if download fails
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Format the file path
        file_path = os.path.join(output_dir, f"{surah_num}_{ayah_num}_{reciter_id}.mp3")
        
        # If file already exists, return its path
        if os.path.exists(file_path):
            logger.info(f"Audio file already exists: {file_path}")
            return file_path
            
        # Construct the URL for the audio file
        audio_url = f"{AUDIO_BASE_URL}/{reciter_id}/{surah_num}_{ayah_num}.mp3"
        
        # Try to get the audio file
        response = requests.get(audio_url, stream=True)
        response.raise_for_status()
        
        # Save the audio file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logger.info(f"Downloaded audio file: {file_path}")
        return file_path
        
    except Exception as e:
        # If we get an error, try to retrieve the original URL from the API
        try:
            logger.warning(f"Error downloading audio from primary source: {e}")
            logger.info("Trying fallback URL...")
            
            # Get ayah details to find the originalUrl
            url = f"{API_BASE_URL}/{surah_num}/{ayah_num}.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Get the original URL for the reciter
            audio_data = data.get('audio', {})
            original_url = audio_data.get(reciter_id, {}).get('originalUrl')
            
            if original_url:
                response = requests.get(original_url, stream=True)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Downloaded audio file from fallback URL: {file_path}")
                return file_path
            else:
                logger.error("No fallback URL available")
                return None
                
        except Exception as inner_e:
            logger.error(f"Failed to download audio: {inner_e}")
            return None


def download_ayah_range(start_ayah: str, end_ayah: str, reciter_id: str, output_dir: str) -> List[str]:
    """
    Download a range of ayahs and return the paths to the downloaded files.
    
    Args:
        start_ayah: Starting ayah in the format 'surah:ayah'
        end_ayah: Ending ayah in the format 'surah:ayah'
        reciter_id: The reciter ID
        output_dir: Directory to save the downloaded audio files
        
    Returns:
        List of paths to the downloaded audio files in sequence
    """
    start_surah, start_ayah_num = parse_ayah_reference(start_ayah)
    end_surah, end_ayah_num = parse_ayah_reference(end_ayah)
    
    # Validate the range
    if start_surah > end_surah or (start_surah == end_surah and start_ayah_num > end_ayah_num):
        raise ValueError("End ayah must come after start ayah")
    
    downloaded_files = []
    
    # If the ayahs are in the same surah
    if start_surah == end_surah:
        for ayah_num in range(start_ayah_num, end_ayah_num + 1):
            file_path = download_ayah_audio(start_surah, ayah_num, reciter_id, output_dir)
            if file_path:
                downloaded_files.append(file_path)
    else:
        # Handle ayahs across multiple surahs
        # First, get the total number of ayahs in the starting surah
        try:
            url = f"{API_BASE_URL}/{start_surah}.json"
            response = requests.get(url)
            response.raise_for_status()
            start_surah_data = response.json()
            total_ayahs_in_start_surah = start_surah_data.get('totalAyah', 0)
            
            # Download remaining ayahs in the starting surah
            for ayah_num in range(start_ayah_num, total_ayahs_in_start_surah + 1):
                file_path = download_ayah_audio(start_surah, ayah_num, reciter_id, output_dir)
                if file_path:
                    downloaded_files.append(file_path)
            
            # Download ayahs from surahs in between
            for surah_num in range(start_surah + 1, end_surah):
                # Get total ayahs in this surah
                url = f"{API_BASE_URL}/{surah_num}.json"
                response = requests.get(url)
                response.raise_for_status()
                surah_data = response.json()
                total_ayahs = surah_data.get('totalAyah', 0)
                
                # Download all ayahs in this surah
                for ayah_num in range(1, total_ayahs + 1):
                    file_path = download_ayah_audio(surah_num, ayah_num, reciter_id, output_dir)
                    if file_path:
                        downloaded_files.append(file_path)
            
            # Download ayahs from the ending surah
            for ayah_num in range(1, end_ayah_num + 1):
                file_path = download_ayah_audio(end_surah, ayah_num, reciter_id, output_dir)
                if file_path:
                    downloaded_files.append(file_path)
                    
        except Exception as e:
            logger.error(f"Error downloading ayah range: {e}")
            raise
    
    return downloaded_files


def get_reciter_id_by_name(reciter_name: str) -> str:
    """
    Get the reciter ID based on the reciter name.
    
    Args:
        reciter_name: The reciter name
        
    Returns:
        The reciter ID
    """
    reciters = get_available_reciters()
    for reciter_id, name in reciters.items():
        if name == reciter_name:
            return reciter_id
    # Default to Mishary Rashid Al Afasy if reciter not found
    return "1"