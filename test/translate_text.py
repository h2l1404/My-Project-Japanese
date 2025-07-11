import os
import json
from googletrans import Translator

def translate_text(text):
    """Translate text to Vietnamese."""
    translator = Translator()
    translated = translator.translate(text, src="ja", dest="vi")
    return translated.text

def translate_json(json_file):
    """Read JSON file, translate text, and save back to JSON."""
    try:
        # Đọc dữ liệu từ file JSON
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Dịch từng đoạn và từng từ
        for segment in data:
            segment["translation"] = translate_text(segment["text"])  # Dịch toàn bộ đoạn
            for word in segment.get("words", []):
                word["translation"] = translate_text(word["surface"])  # Dịch từng từ

        # Lưu kết quả vào cùng file JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Kết quả dịch đã được lưu vào: {json_file}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    # Nhập đường dẫn file JSON từ người dùng
    json_file = input("Nhập đường dẫn file JSON (ví dụ: output/transcription.json): ")
    if not os.path.exists(json_file):
        print("File không tồn tại!")
    else:
        translate_json(json_file)