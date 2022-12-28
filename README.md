# mewzaki

![YouTube Channel Image](https://user-images.githubusercontent.com/91648600/209746946-f24ae679-7f10-4071-b538-bdfcf1a215f2.png)
A script that automatically creates lo-fi variants of randomly selected songs in a Spotify playlist and uploads them to the [mewzaki YouTube channel](https://www.youtube.com/@mewzaki "mewzaki YouTube"). For best results, select songs that have around 80 BPM to avoid excessive distortion.

## How does it work?

1. The user provides a Spotify playlist URI and two songs are randomly selected to convert to their lofi-counterparts using `Spotipy`.
2. YouTube is queried using `youtubesearchpython` to determine links for each of the two songs.
3. The audio from the respective video from each link is downloaded to the audio_files_input directory using `yt-dlp`.
4. Each audio file has their vocals separated from their instrumental using `spleeter`, writing to new audio files in the audio_output directory.
5. The BPM for each track is calculated using `aubio`.
6. Randomly select a beat from the beats_library directory.
7. Alter the vocals to match the BPM of the chosen beat using `pydub`.
8. Overlay the transformed vocals on top of the lofi-beat using `pydub` and write the final audio to a new mp3 file.
9. Combine the audio and the background video using `moviepy`.
10. Upload the video to the _mewzaki_ YouTube channel using `google_auth` related API.

## Next steps

### Scheduling Periodic Uploads

By using Windows Scheduler and converting the `generate_vid_and_upload.py` script into a Batch file, we can set this script to run automatically through a desired time frame.

See the steps here for more info: [How to Schedule Python Script using Windows Scheduler.](https://datatofish.com/python-script-windows-scheduler/#:~:text=Double%2Dclick%20on%20the%20Task,Python%20script%20daily%20at%206am.)

### Deleting Files After Processing

After each video is uploaded, the files used during processing should be discarded to free up space. This is especially important in the case where the script is run periodically, as storage can become a concern without manual maintenance.
