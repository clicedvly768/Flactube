import os
import sys
import platform
import subprocess
import requests
import zipfile
import tarfile
import yt_dlp
from pathlib import Path

def setup_ffmpeg():
    ffmpeg_path = None
    
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return None  
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    ffmpeg_dir = Path(__file__).parent / "ffmpeg"
    ffmpeg_dir.mkdir(exist_ok=True)
    
    if system == "windows":
        ffmpeg_zip = ffmpeg_dir / "ffmpeg.zip"
        url = "https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-full_build.zip"
        
        print("Download FFmpeg for Windows...")
        download_file(url, ffmpeg_zip)
        
        print("Unzip FFmpeg...")
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        for root, _, files in os.walk(ffmpeg_dir):
            if "ffmpeg.exe" in files:
                ffmpeg_path = Path(root) / "ffmpeg.exe"
                break
        
        ffmpeg_zip.unlink()
        
    elif system == "linux":
        print("Install FFmpeg via you packet manage...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
            subprocess.run(["sudo", "pacman", "-Sy"], check=True)
            subprocess.run(["sudo", "pacman", "-S", "ffmpeg"], check=True)
            subprocess.run(["sudo", "dnf", "install", "ffmpeg"], check=True)
            return None
        except subprocess.CalledProcessError:
            print("Failed to install via apt, pacman, dnf let's try downloading...")
            ffmpeg_tar = ffmpeg_dir / "ffmpeg.tar.xz"
            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
            
            download_file(url, ffmpeg_tar)
            
            with tarfile.open(ffmpeg_tar, 'r:xz') as tar_ref:
                tar_ref.extractall(ffmpeg_dir)
            
            for root, _, files in os.walk(ffmpeg_dir):
                if "ffmpeg" in files:
                    ffmpeg_path = Path(root) / "ffmpeg"
                    ffmpeg_path.chmod(0o755)  
                    break
            
            ffmpeg_tar.unlink()
    
    elif system == "darwin":  
        print("Trying to install FFmpeg via Homebrew...")
        try:
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            return None
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Homebrew is not installed, we use binary build...")
            ffmpeg_zip = ffmpeg_dir / "ffmpeg.zip"
            url = "https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip"
            
            download_file(url, ffmpeg_zip)
            
            with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            ffmpeg_path = ffmpeg_dir / "ffmpeg"
            ffmpeg_path.chmod(0o755)
            
            ffmpeg_zip.unlink()
    
    return ffmpeg_path

def download_file(url, destination):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def download_playlist(playlist_url):
    ffmpeg_path = setup_ffmpeg()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        }],
        'quiet': False,
    }
    
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = str(ffmpeg_path)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    playlist_url = input("Enter the URL of the playlist/misuc YouTube: ")
    download_playlist(playlist_url)