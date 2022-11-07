from moviepy.editor import *
from tkinter.filedialog import *
import os


def removebackgroundfrommp3file():
    file_name = './audio_files/boku_no_pico'
    audio = AudioFileClip(f'{file_name}.mp3')
    audio.write_audiofile('./output/current_audio.wav')
    os.system('spleeter separate ./output/current_audio.wav -o output')


removebackgroundfrommp3file()
