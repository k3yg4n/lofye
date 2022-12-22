import moviepy.editor as mpe

dest_file_name = "dec21.mp4"
dest_file_path = f"./videos/{dest_file_name}"
src_file_name = "waterfall_background.mp4"
src_file_path = f"./background/{src_file_name}"
audio_file_name = "if what do you say move it baby by common was lofi.mp3"
audio_file_path = f"./audio_files/{audio_file_name}"

OUTRO_TIME_IN_SECONDS = 5
FPS = 60


def combine(vid_path, aud_path, out_path, fps=FPS):
    audio_background = mpe.AudioFileClip(aud_path)
    audio_duration = audio_background.duration + OUTRO_TIME_IN_SECONDS
    my_clip = mpe.VideoFileClip(vid_path)
    my_clip = my_clip.loop(duration=audio_duration)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(out_path, fps=fps)


combine(src_file_path, audio_file_path, dest_file_path)
