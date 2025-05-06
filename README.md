# Ayahs Audio Downloader

A simple, user-friendly Streamlit application that allows you to download and combine Quran audio files for specific ayah (verse) ranges.

**Live App:** [Open Streamlit App](https://ayahs-audio-downloader.streamlit.app/)

Docs (made by [DeepWiki](https://dev.to/fallon_jimmy/deepwiki-an-ai-guide-to-github-codebase-mastery-3p5m)): https://deepwiki.com/OdyAsh/ayahs-audio-downloader


## ✨ Features

- 🎧 Download audio files for specific ayah ranges from the Quran
- 👥 Choose from multiple renowned reciters
- 🔄 Automatically concatenate multiple ayahs into a single audio file
- 🎵 Listen to audio directly in your browser
- ⬇️ Download the combined audio file to your device

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.11 (Specific version required due to compatibility issues)
- FFmpeg (Required for audio processing)

### Installation with `uv`

1. **Clone this repository**

   ```
   git clone https://github.com/yourusername/ayahs-audio-downloader.git
   cd ayahs-audio-downloader
   ```

2. **Create a virtual environment with Python 3.11**

   ```
   uv venv --python=python3.11
   ```

3. **Activate the virtual environment**

   Windows:
   ```
   .venv\Scripts\activate
   ```
   
   macOS/Linux:
   ```
   source .venv/bin/activate
   ```

4. **Install the application and its dependencies**

   ```
   uv pip install -e .
   ```

5. **Run the application**

   ```
   streamlit run app.py
   ```

6. **Open your browser**
   
   The application should automatically open in your default web browser. If not, visit:
   ```
   http://localhost:8501
   ```

## 🎯 How to Use

1. **Enter ayah range**: Specify a starting and ending ayah in format `surah:ayah` (e.g., `1:1` for Al-Fatiha, first ayah)
2. **Select reciter**: Choose your preferred reciter from the dropdown list
3. **Generate audio**: Click "Get Audio File" to download and combine the ayahs
4. **Listen or download**: Play the audio directly in your browser or download it to your device

## 📦 Installing FFmpeg

The application requires FFmpeg for audio processing:

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add to your system PATH

**macOS:**
```
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install ffmpeg
```

## 🛠️ Troubleshooting

- **Python 3.12+ Issues**: This application requires Python 3.11 due to compatibility issues with PyDub and newer Python versions
- **Missing Audio**: If an ayah fails to download, try a different reciter
- **FFmpeg Not Found**: Ensure FFmpeg is properly installed and accessible in your PATH

## 📚 Resources

- [Quran API Documentation](https://quranapi.pages.dev)
- [Streamlit Documentation](https://docs.streamlit.io)
- [PyDub Documentation](https://github.com/jiaaro/pydub)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Allah (SWT) - First and foremost
- [Quran API](https://quranapi.pages.dev) for providing access to Quran text and audio files
- All reciters whose beautiful recitations are featured in this app