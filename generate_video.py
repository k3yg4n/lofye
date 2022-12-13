from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os.path 
import glob
import shutil
import moviepy.editor as mpe
from visualizer import *

# #Downloads livewallpaper
# options = Options()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(executable_path=r"D:\SW\chromedriver90\chromedriver.exe",chrome_options=options)

# url= "https://mylivewallpapers.com/nature/evening-waterfall-live-wallpaper/"
# driver.get(url)
# download_button = driver.find_element(By.XPATH,'/html/body/main/div[3]/div[2]/div/div[3]/div[5]/div[1]/ul/li[1]/div[2]/div/div/div/div/div[3]/a ')
# download_button.click()

# time.sleep(8)
# driver.quit()


# #get downloaded file and move it to correct directory
# path = (r"C:\Users\Cindy Peng\Downloads")
# new_path = (r"C:\Users\Cindy Peng\Documents\Code\mewzaki\background")

# folder_path = (r"C:\Users\Cindy Peng\Downloads")
# file_type = (r"\*mp4")
# files = glob.glob(folder_path + file_type)
# max_file = max(files, key=os.path.getctime)

# shutil.move(max_file,new_path)

dest_file_name = "dec12.mp4"
dest_file_path = f"./videos/{dest_file_name}"
src_file_name = "long_background.mp4"
src_file_path = f"./background/{src_file_name}"
audio_file_name = "kendrick.mp3"
audio_file_path = f"./audio_files/{audio_file_name}"
FPS = 10

def combine(vid_path, aud_path, out_path, fps=FPS):
    audio_background = mpe.AudioFileClip(aud_path)
    audio_duration = audio_background.duration
    my_clip = mpe.VideoFileClip(vid_path).set_duration(audio_duration)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(out_path, fps=fps)

combine(src_file_path, audio_file_path, dest_file_path)    


# filename = "kendrick.mp3"

# analyzer = AudioAnalyzer()
# visuals = analyzer.load(filename)

# combine("dec7.mp4", "visuals","testervid.mp4")

#merge the song in the background of the mp4
#merge the audio visualizer onto the mp4 with the song 
