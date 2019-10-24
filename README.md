# avel: Audio & Video Editing Library

## Overview

avel is a library of functions for video editing and generation. It supports trimming, combining video clips with different dimensions, adding text overlays, merging audio, and more. 

## Installation

You must have [Python 3](https://www.python.org/downloads/) and [ffmpeg](https://ffmpeg.org/download.html) installed on your machine. Ensure that both `ffmpeg` and `ffprobe` are available from the command line.
To install `avel` run:

```
pip install git+https://github.com/evliang/avel.git
```

## Video library functions

Create clips of a video (original video is preserved):
```Python
from avel.video_lib import trim_video

trim_video(f'input.mp4', 'output0.mp4', 4, 8)
trim_video(f'input.mp4', 'output1.mp4', '00:00:42.000', '00:01:33.700')
trim_video(f'input.mp4', 'output2.mp4', 93.472, 121.337)

# alternatively...with a list of timestamps:
timestamps = [
    '4-8',
    '00:00:42.000-00:01:33.700',
    '93.472-121.337' ]
for (i, t) in enumerate(timestamps):
    trim_video(f'input.mp4', f'output{i}.mkv', *t.split('-'))
```

Combine multiple clips into one file:
```Python
from avel.video_lib import combine_videos

combine_videos(["file1.mp4", "file2.mkv", "file3.avi"], "combined.mkv")
```

Create a video with 16:9 ratio, adding a blur effect to the sides (if applicable)
```Python
from avel.video_lib import blur_video

blur_video("combined.mkv", "blurred.mkv")
```

Add text on top of video (e.g. subtitles, watermark)
```Python
from avel.video_lib import create_drawtext_dict, drawtext

overlays = [
    create_drawtext_dict("avel", "right", "bottom", 40),
    create_drawtext_dict("Hello World!", "mid_x", "bottom", 50, enable="between(t,0,8)") ]

drawtext("input.mkv", "output.mkv", overlays)
```

## Audio library functions

Extract audio from a video
```Python
from avel.audio_lib import extract_audio

extract_audio("video.mp4", "audio1.m4a", 15, 30)
```

Combine multiple audio files into one longer audio file, with an 8-second transition
```Python
from avel.audio_lib import combine_video

combine_audio(["audio1.m4a", "audio2.mp3"], "output.mp3", transition_time=8)
```

Merge two audio files into one (e.g. foreground and background)
```Python
from avel.audio_lib import merge_audio

merge_audio("main.mp3", "background.mp3", "output.mp3", vol1=1.0, vol2=0.4)
```

Combine audio and video file into one video file
```Python
from avel.video_lib import combine_audio_video

combine_audio_video(audioPath, videoPath, output_filename)
```