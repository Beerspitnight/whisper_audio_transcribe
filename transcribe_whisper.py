import argparse
import openai
import os
import re
import whisper
import sys

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

client = openai.OpenAI(api_key=api_key)

def srt_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

def chunk_for_srt(response, max_words=2):
    words = response.words
    chunks = []
    for i in range(0, len(words), max_words):
        group = words[i:i + max_words]
        start = group[0].start
        end = group[-1].end
        text = " ".join([w.word.strip() for w in group])
        chunks.append({
            "index": len(chunks) + 1,
            "start": srt_timestamp(start),
            "end": srt_timestamp(end),
            "text": text.strip()
        })
    return chunks

def transcribe_whisper(audio_path, model="whisper-1"):
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return chunk_for_srt(response)

def transcribe_audio(input_file, output_file=None):
    chunks = transcribe_whisper(input_file)
    if output_file:
        with open(output_file, "w") as f:
            for chunk in chunks:
                f.write(f"{chunk['index']}\n")
                f.write(f"{chunk['start']} --> {chunk['end']}\n")
                f.write(f"{chunk['text']}\n\n")
    else:
        for chunk in chunks:
            print(f"{chunk['index']}")
            print(f"{chunk['start']} --> {chunk['end']}")
            print(f"{chunk['text']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using OpenAI Whisper.")
    parser.add_argument("input_file", help="Path to input audio file.")
    parser.add_argument("-o", "--output", help="Path to output text file.")
    args = parser.parse_args()

    transcribe_audio(args.input_file, args.output)
