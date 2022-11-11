import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint

cid = "74386c8bfb28461aa7a25a760d22a099"
secret = "1b69f47c3b094314ae7af4034412714c"

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Global Top Songs URI
playlist_URI = "37i9dQZEVXbNG2KDcFcKOF"
track_uris = [x["track"]["uri"]
              for x in sp.playlist_tracks(playlist_URI)["items"]]
print(track_uris)
print("\n\n")

top_fifty_tracks = []
five_rand_tracks = []

for track in sp.playlist_tracks(playlist_URI)["items"]:

    # Track name
    track_name = track["track"]["name"]
    print(track_name)

    # Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    print(artist_info)

    # Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_genres = artist_info["genres"]
    print(artist_name)
    print(artist_genres)

    # Popularity of the track
    track_pop = track["track"]["popularity"]
    print(track_pop)

    top_fifty_tracks.append(f"{track_name} by {artist_name}")
    print("\n\n")

for i, track in enumerate(top_fifty_tracks, start=1):
    print(f"Track {i}: {track}")
print("\n")

for i in range(1, 6):
    rand_ind = randint(0, 49)
    print(f"rand_ind: {rand_ind}")
    five_rand_tracks.append(top_fifty_tracks[rand_ind])
print("\n")

print("CHOSEN 5 TRACKS: ")
for i, track in enumerate(five_rand_tracks, start=1):
    print(f"Track {i}: {track}")
print("\n")

# For imformation about each track: https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50
