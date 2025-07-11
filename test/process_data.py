import os
import json

def process_data(json_file):
    """Process JSON data into the final format."""
    try:
        # Đọc dữ liệu từ file JSON
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Xử lý dữ liệu thành định dạng cuối cùng
        result = []
        for i, segment in enumerate(data):
            words_info = []
            start_time = segment["start"]
            end_time = segment["end"]
            full_text = segment["text"]
            translated_text = segment.get("translation", "")  # Lấy bản dịch nếu có

            # Xử lý từng từ
            words = full_text.split()
            word_duration = (end_time - start_time) / len(words)
            for j, word in enumerate(words):
                word_start = start_time + j * word_duration
                word_end = start_time + (j + 1) * word_duration
                word_translation = ""
                for w in segment.get("words", []):
                    if w["surface"] == word:
                        word_translation = w.get("translation", "")
                        break
                words_info.append({
                    "surface": word,
                    "translation": word_translation,
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

        # Lưu kết quả vào file JSON
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "final_output.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print(f"Kết quả đã được lưu vào: {output_file}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    # Nhập đường dẫn file JSON từ người dùng
    json_file = input("Nhập đường dẫn file JSON (ví dụ: output/transcription.json): ")
    if not os.path.exists(json_file):
        print("File không tồn tại!")
    else:
        process_data(json_file)