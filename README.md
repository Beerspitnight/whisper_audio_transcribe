# Whisper Audio Transcribe

A Python script to transcribe audio files using OpenAI's Whisper API. Outputs clean text or time-stamped captions (SRT-style).

## Features
- Transcribes audio (MP3, etc) to text
- Outputs to console or file
- SRT-style word-level timestamps
- Configurable word chunk size for captions

## Requirements
- Python 3.x
- `openai`
- `whisper`
- `argparse`

## Installation
```bash
pip install openai whisper

## Usage
-First, set your API key:

export OPENAI_API_KEY="your-openai-api-key"

-Then run:

python transcribe_whisper.py input.mp3
python transcribe_whisper.py input.mp3 -o output.srt
