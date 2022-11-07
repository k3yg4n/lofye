import youtube_dl
import os


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
    'outtmpl': 'audio_files/%(title)s.%(ext)s',
    # 'writeinfojson' # Use this if we want to write to a JSON and store it in a database
}


def download_audio(yt_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=yt_url, download=False)
        filename = f"{video_info['title']}.mp3"
        print(f"DOWNLOADING: {filename}")
        print(f"DURATION: {video_info['duration']} seconds")
        print(list(video_info))
        ydl.download([yt_url])


download_audio('https://www.youtube.com/watch?v=CZQDzD_bzZQ')