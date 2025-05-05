# Project Setup Guide

This guide provides instructions on how to set up the Ayahs Audio Downloader project using the `uv` tool.

## Prerequisites

- **Python 3.11** (Note: There is a known issue with pydub/pyaudiooop in Python 3.12+ - see troubleshooting section)
- [uv](https://github.com/astral-sh/uv) - Modern Python package installer and resolver
- FFmpeg (required for audio processing with pydub)

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd ayahs-audio-downloader
```

2. Create a virtual environment using uv with Python 3.11:

```bash
uv venv --python=python3.11
```

3. Activate the virtual environment:

```bash
# On Windows:
.venv\Scripts\activate
```

```bash
# On Unix/macOS:
source .venv/bin/activate
```

4. Install the package in development mode:

```bash
uv pip install -e .
```

5. Verify installation:

```bash
python -c "import streamlit, requests, pydub; print('All dependencies installed successfully!')"
```

## Project Structure

```
ayahs-audio-downloader/
├── app.py               # Main Streamlit application
├── packages.txt         # External dependencies for Streamlit Cloud
├── pyproject.toml       # Project configuration and dependencies
├── README.md            # Project documentation
├── src/                 # Source code package
│   ├── __init__.py      # Makes src a Python package
│   ├── audio_downloader.py  # Functions to download Quran audio files
│   └── audio_processor.py   # Functions to process and concatenate audio files
├── temp_data/           # Temporary storage for downloaded audio files
└── output/              # Directory for final concatenated audio files
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

This will start the application and open it in your default web browser.

## Development

For development, you can install the development dependencies:

```bash
uv pip install -e ".[dev]"
```

This will install development tools like pytest, black, and isort.

## Note on FFmpeg

The audio processing functionality requires FFmpeg to be installed on your system:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: Install via Homebrew: `brew install ffmpeg`
- **Linux**: Install via package manager: `apt install ffmpeg` or equivalent

## Troubleshooting

### No module named 'pyaudiooop' error

There's a known issue with pydub on Python 3.12+ where it tries to import a module that no longer exists in the standard library. If you encounter this error:

```
ImportError: No module named 'pyaudiooop'
```

The recommended solution is to use Python 3.11, as specified in the setup instructions above.

This issue is tracked in pydub here: https://github.com/jiaaro/pydub/issues/725

### Deployment to Streamlit Cloud

When deploying to Streamlit Cloud, the packages.txt file will ensure that FFmpeg is installed automatically. No additional configuration is needed.