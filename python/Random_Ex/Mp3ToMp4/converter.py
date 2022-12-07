#! /usr/bin/env python
import glob
from moviepy.editor import *
from pathlib import Path

imagePath = r''
outputPath = r''
mp3FilesPath = r''

# for filepath in glob.iglob(r'C:\Users\admin\*.png', recursive=True):
for filepath in glob.iglob(mp3FilesPath):
    # join output path with cotout of mp3 file name
    output = outputPath+Path(filepath).stem

    # initialize audio clip, and image clip with duration of audio
    audioclip = AudioFileClip(filepath)
    imageClip = ImageClip(imagePath, duration=audioclip.duration)

    # add audio to image clip
    imageClip = imageClip.set_audio(audioclip)

    # export image clip as an mp4 file
    imageClip.write_videofile(output+'.mp4', fps=24)
