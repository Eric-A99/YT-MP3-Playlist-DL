from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_to_mp3(input_file, output_file):
    try:
        logging.info(f"Converting {input_file} to {output_file}")
        result = subprocess.run(['ffmpeg', '-i', input_file, output_file], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"ffmpeg error: {result.stderr}")
            return False
        os.remove(input_file)  # Remove the original file
        logging.info(f"Removed original file {input_file}")
        return True
    except Exception as e:
        logging.error(f"Error converting file: {e}", exc_info=True)
        return False

def download_audio(video, download_path):
    try:
        logging.info(f"Fetching video: {video.title}")
        audio_stream = video.streams.get_audio_only()
        if not audio_stream:
            logging.error("No audio stream found.")
            return
        output_file = audio_stream.download(output_path=download_path)
        logging.info(f"Downloaded audio to {output_file}")
        
        # Convert to mp3
        base, ext = os.path.splitext(output_file)
        mp3_file = base + '.mp3'
        if convert_to_mp3(output_file, mp3_file):
            logging.info(f"Converted to MP3: {mp3_file}")
    except Exception as e:
        logging.error(f"Error downloading audio: {e}", exc_info=True)

def download_track(url, download_path):
    yt = YouTube(url, on_progress_callback=on_progress)
    download_audio(yt, download_path)

def download_playlist(url, download_path):
    pl = Playlist(url)
    for video in pl.videos:
        download_audio(video, download_path)

# Define download path
download_path = "/Users/eric-a99/Desktop/YouTube Downloads"
if not os.path.exists(download_path):
    logging.error(f"Download path {download_path} does not exist.")
    exit(1)

# User choice
choice = input("Enter 'T' to download a single track or 'P' to download a playlist: ").strip().upper()

if choice == 'T':
    track_url = input("Enter the YouTube track URL: ").strip()
    download_track(track_url, download_path)
elif choice == 'P':
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    download_playlist(playlist_url, download_path)
else:
    logging.error("Invalid choice. Please enter 'T' for a single track or 'P' for a playlist.")
