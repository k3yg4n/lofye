# To query Spotify using Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import random

# To complete YouTube search
from youtubesearchpython import VideosSearch

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

# BPM Calculations
from aubio import source, tempo
from numpy import median, diff

# Vocal manipulations
from pydub import AudioSegment


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
        'preferredcodec': 'wav',
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
        filename = f"{video_info['id']}.wav"
        print(f"DOWNLOADING {filename}...")
        # print(f"DURATION: {video_info['duration']} seconds")
        # print(list(video_info)) # TO SEE FIELDS WE CAN READ...
        ydl.download([yt_url])
        return video_info['id']


def removeBackgroundFromAudioFile(file_name):
    file_path = f"./audio_files/{file_name}.wav"
    audio = AudioFileClip(file_path)
    audio.write_audiofile(f'./output/{file_name}.wav')
    os.system(f'spleeter separate ./output/{file_name}.wav -o output')


def replaceInvalidChars(file_name):
    file_name = unicodedata.normalize('NFKD', file_name).encode(
        'ascii', 'ignore').decode('ascii')
    file_name = re.sub(r'[^\w\s-]', '', file_name.lower())
    return re.sub(r'[-\s]+', '-', file_name).strip('-_')


def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            # if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)


def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


# Spotify Keys
cid = "74386c8bfb28461aa7a25a760d22a099"
secret = "1b69f47c3b094314ae7af4034412714c"

# Spotify Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Spotify Playlist URIs
TOP_50_URI = "37i9dQZEVXbNG2KDcFcKOF"
FONI_URI = "56j8LKCvUH4kyEHHQW5Dge"
LYRICAL_RAP_URI = "1tK3uHXK80UfIOjPdDxkiQ"
EIGHTY_BPM_URI = "2Cxy4eFOnkDpWA7je1VIAZ"
JAZZ_RAP_URI = "37i9dQZF1DX8Kgdykz6OKj"

CURRENT_PLAYLIST_URI = JAZZ_RAP_URI

# Beats Library
beats_library = {
    "60BPM": {"file_name": "60BPM.mp3", "bpm": 60},
    "75BPM": {"file_name": "75BPM.mp3", "bpm": 75},
    "85BPM": {"file_name": "85BPM.mp3", "bpm": 85},
}

track_uris = [x["track"]["uri"]
              for x in sp.playlist_tracks(CURRENT_PLAYLIST_URI)["items"]]  # List of track URIs
# print(track_uris)
# print("\n\n")

top_fifty_tracks = []
five_rand_tracks = []
tracks_data_struct = {}

for track in sp.playlist_tracks(CURRENT_PLAYLIST_URI)["items"]:

    # Track name
    # print(track["track"])
    track_name = track["track"]["name"]
    # print(track_name)

    # Main Artist
    #  artist_uri = track["track"]["artists"][0]["uri"]
    #  artist_info = sp.artist(artist_uri)
    # print(artist_info)

    # Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    # artist_genres = artist_info["genres"]
    # print(artist_name)
    # print(artist_genres)

    # Popularity of the track
    # track_pop = track["track"]["popularity"]
    # print(track_pop)

    top_fifty_tracks.append(replaceInvalidChars(
        f"{track_name} by {artist_name}"))
    # print("\n\n")

for i, track in enumerate(top_fifty_tracks, start=1):
    print(f"Track {i}: {track}")
print("\n")

for i in range(1, 6):
    rand_track = top_fifty_tracks.pop(random.randrange(len(top_fifty_tracks)))
    five_rand_tracks.append(rand_track)
print("\n")

# FOR TESTING PURPOSES:
# five_rand_tracks.append("not-the-only-one-by-sam-smith")
# five_rand_tracks.append("too-good-at-goodbyes-by-sam-smith")
# five_rand_tracks.append("stereo-hearts-by-gym-class-heroes")
# five_rand_tracks.append("positions-by-ariana-grande")
# five_rand_tracks.append("4-your-eyes-only-by-j.cole")
# five_rand_tracks.append("doomsday-by-mf-doom")

print("CHOSEN 5 TRACKS: ")
for i, track in enumerate(five_rand_tracks, start=1):
    print(f"Track {i}: {track}")
print("\n")

for i, track in enumerate(five_rand_tracks, start=1):
    print(f"Currently Downloading Track {i}: {track}")

    # Obtain the YouTube link of each of the five tracks
    videosSearch = VideosSearch(f"{track} audio", limit=1)
    results_obj = videosSearch.result()
    yt_video = results_obj["result"][0]
    yt_link = yt_video["link"]
    print(f"Track {i} Link: {yt_link}")

    # Download each track
    vid_id = download_audio(yt_link)
    tracks_data_struct[track] = {'id': vid_id}
    print(tracks_data_struct)

    # Separate vocals from instrumental
    removeBackgroundFromAudioFile(vid_id)

    print("\n")

# Navigate to the output directory
os.chdir("output")

for track in tracks_data_struct:
    yt_id = tracks_data_struct[track]['id']
    for filename in os.listdir():
        # Rename audio files
        if yt_id in filename and filename.endswith(".wav"):
            print(f"Renaming... {filename} -> {track}.wav")
            os.rename(filename, f"{track}.wav")
        # Rename folders
        elif yt_id in filename:
            print(f"Renaming... {filename} -> {track}")
            os.rename(filename, track)
print("\n")

# Calculate the BPM for each track and add to data struct
print("Calculating BPM...")
for track in tracks_data_struct:
    current_file = f"{track}.wav"
    bpm = get_file_bpm(f"./{current_file}")
    print(f"Current file: {current_file}  BPM: {bpm}")

    tracks_data_struct[track]['bpm'] = bpm
print(tracks_data_struct)
print("\n")

# Select a beat...
chosen_beat = random.choice(list(beats_library.keys()))
print(f"Selected beat: {beats_library[chosen_beat]['file_name']}")
lofi_beat = (AudioSegment.from_file(
    f"../beats_library/{beats_library[chosen_beat]['file_name']}") * 10) - 3
beat_bpm = beats_library[chosen_beat]['bpm']

# Slow vocals accordingly
print("Slowing vocals...")
for track in tracks_data_struct:
    vocals = AudioSegment.from_file(f"./{track}/vocals.wav") - 15
    song_bpm = tracks_data_struct[track]["bpm"]

    # Slow the vocals to achieve the same bpm as the beat
    slow_vocals = speed_change(vocals, beat_bpm / song_bpm)
    slow_vocals.export(f"./{track}/slow_vocals.mp3", format="mp3")

    # Create the track by overlaying the beat over the slow vocals
    lofi_track = slow_vocals.overlay(lofi_beat, position=0)
    lofi_track = lofi_track.fade_in(1000).fade_out(3000)
    lofi_track.export(
        f"./{track}/if {track.replace('-',' ')} was lofi.mp3", format="mp3")
