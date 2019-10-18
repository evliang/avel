# avel: Audio & Video Editing Library

## Overview

avel is a library of functions for video editing and generation. It supports trimming, combining video clips with different dimensions, adding text overlays, merging audio, and more. 

## Installation

You must have [Python 3](https://www.python.org/downloads/) and [ffmpeg](https://ffmpeg.org/download.html) installed on your machine. Ensure that both `ffmpeg` and `ffprobe` are available from the command line.
To install `avel` run:

```
pip install git+https://github.com/evliang/avel.git
```

## Example Usages

```Python
from avel import video_lib, audio_lib
```

```Python
### create clips of a video (original video is preserved)
video_lib.trim_video(f'input.mp4', 'output0.mp4', 4, 8)
video_lib.trim_video(f'input.mp4', 'output1.mp4', '00:00:42.000', '00:01:33.700')
video_lib.trim_video(f'input.mp4', 'output2.mp4', 93.472, 121.337)
```

### alternatively...if you have a list of timestamps coming from another process...
```Python
timestamps = [
    '4-8',
    '00:00:42.000-00:01:33.700',
    '93.472-121.337' ]
for (i, t) in enumerate(timestamps):
    video_lib.trim_video(f'input.mp4', f'output{i}.mkv', *t.split('-'))
```

### combine multiple clips into one file
```Python
video_lib.combine_videos(["file1.mp4", "file2.mkv", "file3.avi"], "combined.mkv")
```

### creates a video with 16:9 ratio, adding a blur effect to the sides if applicable
```Python
video_lib.blur_video("combined.mkv", "blurred.mkv")
```

### extract audio from a video
```Python
audio_lib.extract_audio("video.mp4", "audio1.m4a", 15, 30)
```

### combine multiple audio files into one longer audio file, with 8s transition
```Python
audio_lib.combine_audio(["audio1.m4a", "audio2.mp3"], "output.mp3", transition_time=8)
```

### merge two audio files into one
```Python
audio_lib.merge_audio("main.mp3", "background.mp3", "output.mp3", vol1=1.0, vol2=0.4)
```

# combine audio and video file into one video file
```Python
combine_audio_video(audioPath, videoPath, output_filename)
```
