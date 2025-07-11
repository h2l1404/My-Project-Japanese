import yt_dlp
import os

def download_audio_from_youtube(url, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = os.path.join(output_dir, f"{info['id']}.mp3")
            return audio_file
    except Exception as e:
        print(f"Lỗi khi tải audio: {e}")
        return None

if __name__ == "__main__":
    youtube_url = input("Nhập URL của video YouTube: ").strip()
    if not youtube_url.startswith("https://www.youtube.com/"):
        print("URL không hợp lệ! Vui lòng nhập URL bắt đầu bằng 'https://www.youtube.com/ '.")
    else:
        try:
            audio_file = download_audio_from_youtube(youtube_url)
            if audio_file:
                print(f"Audio đã được tải xuống: {audio_file}")
            else:
                print("Không thể tải audio.")
        except Exception as e:
            print(f"Lỗi: {e}")