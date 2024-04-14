#!/usr/bin/env python3

import os
from pytube import YouTube
import ssl

def download_audio(url):
    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    output_path = os.path.expanduser('~/Desktop/YouTube Downloads')
    audio.download(output_path=output_path, filename_prefix='audio')
    # Convert the downloaded file to mp3 format
    mp4_file = os.path.join(output_path, f'audio.{audio.default_filename}')
    mp3_file = os.path.join(output_path, f'audio.mp3')
    audio_file = os.path.join(output_path, f'audio.{audio.default_filename}')
    os.rename(audio_file, mp3_file)
    
    print("Nice Rip")  # Print statement added

if __name__ == '__main__':
    url = input('Enter YouTube URL: ')
    download_audio(url)
