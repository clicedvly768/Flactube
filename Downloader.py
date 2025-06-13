import yt_dlp
import os

def download_with_ytdlp(playlist_url, output_dir="downloads"):
    
    ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
    
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        }],
        'ffmpeg_location': ffmpeg_path,
        'quiet': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    playlist_url = input("Write URL Video/Music/Playlist YouTube: ")
    download_with_ytdlp(playlist_url)