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

- **trim_video**: Create clips of a video (original video is preserved)
```Python
trim_video(f'input.mp4', 'output0.mp4', 4, 8.2)
trim_video(f'input.mp4', 'output1.mp4', '00:00:42.000', '00:01:33.700')
```

- **combine_videos**: Combine multiple clips into one file
```Python
combine_videos(["file1.mp4", "file2.mkv", "file3.avi"], "combined.mkv")
```

**blur_video**: Create a video with 16:9 ratio, adding a blur effect to the sides (if applicable)
```Python
blur_video("combined.mkv", "blurred.mkv")
```

**drawtext**: Add text on top of video (e.g. subtitles, watermark) using a dictionary of options
```Python
overlays = [
    create_drawtext_dict("avel", "right", "bottom", 40),
    create_drawtext_dict("Hello World!", "mid_x", "bottom", 50, enable="between(t,0,8)") ]

drawtext("input.mkv", "output.mkv", overlays)
```

## Audio library functions

**extract_audio**: Extract audio from a video
```Python
extract_audio("video.mp4", "audio1.m4a", 15, 30)
```

**combine_audio**: Combine list of audio files into one longer audio file, with an 8-second transition
```Python
combine_audio(["audio1.m4a", "audio2.mp3"], "output.mp3", transition_time=8)
```

**merge_audio**: Merge two audio files into one (e.g. foreground and background)
```Python
merge_audio("main.mp3", "background.mp3", "output.mp3", vol1=1.0, vol2=0.4)
```

**combine_audio_video**: Combine audio and video file into one video file
```Python
combine_audio_video(audioPath, videoPath, output_filename)
```

## Examples

See example folder for some scripts that I created for my own use case