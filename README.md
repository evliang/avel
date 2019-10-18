# avel: Audio & Video Editing Library

## Overview

avel is a library of functions for video editing and generation. It supports trimming, combining video clips with different dimensions, adding text overlays, merging audio, and more.

## Installation

You must have [Python 3](https://www.python.org/downloads/) and [ffmpeg](https://ffmpeg.org/download.html) installed on your machine. Ensure that both `ffmpeg` and `ffprobe` are available from the command line.
To install `avel` run:

```
pip install git+https://github.com/evliang/avel.git
```

## Example Usage

```Python
import avel

# create 3 video clips from an input file and timestamps
timestamps = [
    '4.472-8.337',
    '00:00:42.000-00:01:33.700',
    '93.7'-'121' ]
for (i, t) in enumerate(timestamps):
    avel.video_lib.trim_video(f'input.mp4', f'output{i}.mkv', *t.split('-'))
```

See the examples folder for more use cases
