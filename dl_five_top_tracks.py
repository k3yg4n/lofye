# To query Spotify using Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randrange

# To complete YouTube search
from youtubesearchpython import VideosSearch
import pprint

# For downloading mp3s
# import youtube_dl
import yt_dlp

# For vocal separation
from moviepy.editor import *
from tkinter.filedialog import *
import os

# For string manipulations
import unicodedata
import re

# For downloading mp3s


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


# The video download settings/options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': 'audio_files/%(id)s.%(ext)s',
    # 'writeinfojson' # Use this if we want to write to a JSON and store it in a database
}


def download_audio(yt_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=yt_url, download=False)
        filename = f"{video_info['id']}.mp3"
        print(f"DOWNLOADING... Current file (yt_id.mp3): {filename}")
        # print(f"DURATION: {video_info['duration']} seconds")
        print(list(video_info))
        ydl.download([yt_url])
        return video_info['id']


def removeBackgroundFromMp3File(file_name):
    file_path = f"./audio_files/{file_name}.mp3"
    audio = AudioFileClip(file_path)
    audio.write_audiofile(f'./output/{file_name}.mp3')
    os.system(f'spleeter separate ./output/{file_name}.mp3 -o output')


def replaceInvalidChars(file_name):
    file_name = unicodedata.normalize('NFKD', file_name).encode(
        'ascii', 'ignore').decode('ascii')
    file_name = re.sub(r'[^\w\s-]', '', file_name.lower())
    return re.sub(r'[-\s]+', '-', file_name).strip('-_')


# Spotify Keys
cid = "74386c8bfb28461aa7a25a760d22a099"
secret = "1b69f47c3b094314ae7af4034412714c"

# Spotify Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Global Top Songs URI
playlist_URI = "37i9dQZEVXbNG2KDcFcKOF"
track_uris = [x["track"]["uri"]
              for x in sp.playlist_tracks(playlist_URI)["items"]]  # List of track URIs
# print(track_uris)
# print("\n\n")

top_fifty_tracks = []
five_rand_tracks = []
tracks_and_ids = {}

for track in sp.playlist_tracks(playlist_URI)["items"]:

    # Track name
    track_name = track["track"]["name"]
    # print(track_name)

    # Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    # print(artist_info)

    # Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_genres = artist_info["genres"]
    # print(artist_name)
    # print(artist_genres)

    # Popularity of the track
    track_pop = track["track"]["popularity"]
    # print(track_pop)

    top_fifty_tracks.append(replaceInvalidChars(
        f"{track_name} by {artist_name}"))
    # print("\n\n")

for i, track in enumerate(top_fifty_tracks, start=1):
    print(f"Track {i}: {track}")
print("\n")

# for i in range(1, 6):
#     rand_track = top_fifty_tracks.pop(randrange(len(top_fifty_tracks)))
#     five_rand_tracks.append(rand_track)
#     tracks_and_ids[rand_track] = ""
# print("\n")

# FOR TESTING PURPOSES:
five_rand_tracks.append("anti-hero-by-taylor-swift")
five_rand_tracks.append("rich-flex-by-drake")
five_rand_tracks.append("unholy-feat-kim-petras-by-sam-smith")
five_rand_tracks.append("major-distribution-by-drake")
five_rand_tracks.append("pussy-millions-feat-travis-scott-by-drake")


print("CHOSEN 5 TRACKS: ")
for i, track in enumerate(five_rand_tracks, start=1):
    print(f"Track {i}: {track}")

print("NEW OBJECT: ")
print(tracks_and_ids)
print("\n")

for i, track in enumerate(five_rand_tracks, start=1):
    print(f"Currently Downloading Track {i}: {track}")

    # Obtain the YouTube link of each of the five tracks
    videosSearch = VideosSearch(track, limit=1)
    results_obj = videosSearch.result()
    yt_video = results_obj["result"][0]
    yt_link = yt_video["link"]
    print(f"Track {i} Link: {yt_link}")

    # Download each track
    vid_id = download_audio(yt_link)
    tracks_and_ids[track] = vid_id
    print(tracks_and_ids)

    # Separate vocals from instrumental
    removeBackgroundFromMp3File(vid_id)

    print("\n")

# Navigate to the output directory
os.chdir("output")
for track in tracks_and_ids:
    yt_id = tracks_and_ids[track]
    for filename in os.listdir():
        print(f"Current ID: {yt_id}")
        print(f"Current file: {filename}")
        if yt_id in filename and filename.endswith(".mp3"):
            print(f"Renaming... {filename} -> {track}.mp3")
            os.rename(filename, f"{track}.mp3")
        elif yt_id in filename:
            print(f"Renaming... {filename} -> {track}")
            os.rename(filename, track)
        print("\n")
