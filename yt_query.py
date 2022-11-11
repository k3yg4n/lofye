from youtubesearchpython import VideosSearch

import pprint

videosSearch = VideosSearch('Hello', limit=2)

results_obj = videosSearch.result()

video1 = results_obj["result"][0]
yt_link = video1["link"]

print("VIDEO 1:")
pprint.pprint(video1)
print("\n\n\n")
print(f"Link: {yt_link}")
