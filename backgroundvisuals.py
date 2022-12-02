
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

#Downloads livewallpaper
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=r"D:\SW\chromedriver90\chromedriver.exe",chrome_options=options)

url= "https://mylivewallpapers.com/nature/evening-waterfall-live-wallpaper/"
driver.get(url)
download_button = driver.find_element(By.XPATH,'/html/body/main/div[3]/div[2]/div/div[3]/div[5]/div[1]/ul/li[1]/div[2]/div/div/div/div/div[3]/a ')
download_button.click()

time.sleep(8)
driver.quit()


#get downloaded file and move it to correct directory
path = (r"C:\Users\Cindy Peng\Downloads")
new_path = (r"C:\Users\Cindy Peng\Documents\Code\mewzaki\background")

folder_path = (r"C:\Users\Cindy Peng\Downloads")
file_type = (r"\*mp4")
files = glob.glob(folder_path + file_type)
max_file = max(files, key=os.path.getctime)

shutil.move(max_file,new_path)


def combine(vidname, audname, outname, fps=60):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)


combine("mylivewallpapers-com-Evening-Waterfall-4K (1).mp4","kendrick.mp3", "test.mp4")    


#loop the mp4 to meet song length
#merge the song in the background of the mp4
#merge the audio visualizer onto the mp4 with the song 
