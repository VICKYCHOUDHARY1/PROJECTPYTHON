import tkinter as tk
from datetime import datetime
import sqlite3
import pygame
import yt_dlp
from youtube_search import YoutubeSearch
import os

class MusicBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Bot")

        # Create song entry field
        self.song_label = tk.Label(self.root, text="Enter a song name:")
        self.song_label.pack()
        self.song_entry = tk.Entry(self.root)
        self.song_entry.pack()

        # Create play button
        self.play_button = tk.Button(self.root, text="Play", command=self.play_song)
        self.play_button.pack()

        # Create download audio button
        self.download_audio_button = tk.Button(self.root, text="Download Audio", command=self.download_audio)
        self.download_audio_button.pack()

        # Create download video button
        self.download_video_button = tk.Button(self.root, text="Download Video", command=self.download_video)
        self.download_video_button.pack()

    def play_song(self):
        # Get song name from entry field
        song_name = self.song_entry.get()

        # Search for the song on YouTube
        results = YoutubeSearch(song_name, max_results=1).to_dict()

        if results:
            # Get the URL of the first result
            url = "https://www.youtube.com" + results[0]["url_suffix"]

            # Use yt-dlp to download the song
            audio_file_path = self.download_song(url)

            if audio_file_path:
                # Play the song using a music player library (e.g., pygame)
                self.play_music(audio_file_path)

                # Store song information in a database or file
                self.store_song_info(song_name)
            else:
                print("Failed to download the song.")
        else:
            print("Song not found")

    def download_audio(self):
        # Get song name from entry field
        song_name = self.song_entry.get()

        # Search for the song on YouTube
        results = YoutubeSearch(song_name, max_results=1).to_dict()

        if results:
            # Get the URL of the first result
            url = "https://www.youtube.com" + results[0]["url_suffix"]

            # Use yt-dlp to download the song
            audio_file_path = self.download_song(url)

            if audio_file_path:
                print("Audio downloaded successfully.")
            else:
                print("Failed to download the audio.")
        else:
            print("Song not found")

    def download_video(self):
        # Get song name from entry field
        song_name = self.song_entry.get()

        # Search for the song on YouTube
        results = YoutubeSearch(song_name, max_results=1).to_dict()

        if results:
            # Get the URL of the first result
            url = "https://www.youtube.com" + results[0]["url_suffix"]

            # Use yt-dlp to download the video
            video_file_path = self.download_video_file(url)

            if video_file_path:
                print("Video downloaded successfully.")
            else:
                print("Failed to download the video.")
        else:
            print("Song not found")

    def download_song(self, url):
        try:
            # Use yt-dlp to download the song
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                audio_file_path = ydl.prepare_filename(info_dict)
                return audio_file_path
        except Exception as e:
            print(f"Error downloading song: {e}")
            return None

    def download_video_file(self, url):
        try:
            # Use yt-dlp to download the video
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_file_path = ydl.prepare_filename(info_dict)
                return video_file_path
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

    def play_music(self, audio_file_path):
        # Initialize pygame mixer
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()

        # Keep the program running while the music is playing
        while pygame.mixer.music.get_busy():
            self.root.update()  # Update the Tkinter window

    def store_song_info(self, song_name):
        # Store song information in a database or file
        conn = sqlite3.connect("song_database.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS songs (song_name TEXT, played_at TEXT)")
        c.execute("INSERT INTO songs (song_name, played_at) VALUES (?, ?)", (song_name, datetime.now()))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Create downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    bot = MusicBot()
    bot.root.mainloop()

#bot is running on windows and running in a different process than the surrent server is lentitly runnign anf it is runnning like a :
#hhtps server and the server that is not bypassing the currnet server 