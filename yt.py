import os
import subprocess
from pytube import YouTube

url = input("Enter YouTube URL: ")

try:
    yt = YouTube(url)
except Exception as e:
    print(f"Error accessing video: {e}")
    exit(1)

download_path = "/Users/eric-a99/Desktop/YouTube Downloads"
if not os.path.exists(download_path):
    print(f"Download path {download_path} does not exist.")
    exit(1)

try:
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.default_filename
    stream.download(download_path)

    # Convert the downloaded audio to .mp3 format
    webm_file = os.path.join(download_path, filename)
    mp3_file = os.path.join(download_path, os.path.splitext(filename)[0] + '.mp3')
    subprocess.run(['ffmpeg', '-i', webm_file, '-vn', '-ab', '128k', '-ar', '44100', '-y', mp3_file])

    # Delete the original .webm file
    os.remove(webm_file)

    print("Nice Rip!")
except Exception as e:
    print(f"Error downloading audio: {e}")
    exit(1)