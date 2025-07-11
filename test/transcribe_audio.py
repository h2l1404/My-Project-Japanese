import whisper
import os
import json

def transcribe_audio(audio_file):
    """Transcribe audio file to text using Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, language="ja", verbose=False)
    return result["segments"]  # Return segments with timestamps

if __name__ == "__main__":
    # Nhập đường dẫn file audio từ người dùng
    audio_file = input("Nhập đường dẫn file audio (ví dụ: output/VIDEO_ID.mp3): ")
    if not os.path.exists(audio_file):
        print("File không tồn tại!")
    else:
        try:
            # Thực hiện transcription
            segments = transcribe_audio(audio_file)

            # Lưu kết quả vào file JSON
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục output nếu chưa tồn tại
            output_file = os.path.join(output_dir, "transcription.json")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(segments, f, ensure_ascii=False, indent=4)

            print(f"Kết quả transcription đã được lưu vào: {output_file}")
        except Exception as e:
            print(f"Lỗi: {e}")