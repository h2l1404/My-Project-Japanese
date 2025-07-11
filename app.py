import os
from flask import Flask, request, jsonify
from pytube import YouTube
import whisper
from googletrans import Translator
import json

app = Flask(__name__)

# Directory to store audio and JSON files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Whisper model for transcription
model = whisper.load_model("base")

# Initialize Google Translate client
translator = Translator()

def download_audio_from_youtube(url):
    """Download audio from YouTube and return the file path."""
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = os.path.join(OUTPUT_DIR, f"{yt.video_id}.mp3")
    audio_stream.download(output_path=OUTPUT_DIR, filename=f"{yt.video_id}.mp3")
    return audio_file

def transcribe_audio(audio_file):
    """Transcribe audio file to text using Whisper."""
    result = model.transcribe(audio_file, language="ja", verbose=False)
    return result["segments"]  # Return segments with timestamps

def translate_text(text):
    """Translate text to Vietnamese."""
    translated = translator.translate(text, src="ja", dest="vi")
    return translated.text

def process_transcription(segments):
    """Process transcription segments into the desired JSON format."""
    result = []
    for i, segment in enumerate(segments):
        words_info = []
        start_time = segment["start"]
        end_time = segment["end"]
        full_text = segment["text"]
        translated_text = translate_text(full_text)

        # Split text into words and assign approximate timestamps
        words = full_text.split()
        word_duration = (end_time - start_time) / len(words)
        for j, word in enumerate(words):
            word_start = start_time + j * word_duration
            word_end = start_time + (j + 1) * word_duration
            words_info.append({
                "surface": word,
                "translation": translate_text(word),
                "start_time": word_start,
                "end_time": word_end
            })

        result.append({
            "id": i,
            "seek": 0,
            "start": start_time,
            "end": end_time,
            "text": full_text,
            "translated_text": translated_text,
            "words": words_info
        })

    return result

@app.route('/process', methods=['POST'])
def process():
    """API endpoint to process YouTube video."""
    data = request.json
    youtube_url = data.get("url")

    if not youtube_url:
        return jsonify({"error": "YouTube URL is required"}), 400

    try:
        # Step 1: Download audio
        audio_file = download_audio_from_youtube(youtube_url)

        # Step 2: Transcribe audio
        transcription_segments = transcribe_audio(audio_file)

        # Step 3: Process transcription
        json_output = process_transcription(transcription_segments)

        # Step 4: Save JSON output
        output_file = os.path.join(OUTPUT_DIR, "output.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(json_output, f, ensure_ascii=False, indent=4)

        return jsonify({"status": "success", "data": json_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)