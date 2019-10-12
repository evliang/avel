import os
import uuid
import shutil
import subprocess
from shared_lib import get_duration

def _pad_integer(i):
    return str(i).zfill(2)

def combine_audio(audio_list, output_path, transition_time=13, debugging=False):
    """Creates a single audio file from a list"""
    temp0 = os.path.join(os.path.dirname(output_path), 'temp0.wav')
    temp1 = os.path.join(os.path.dirname(output_path), 'temp1.wav')
    def temp_file(i):
        if i % 2 == 0:
            return temp0
        else:
            return temp1
    if len(audio_list) > 2:
        print(audio_list)
        subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', audio_list[0], '-i', audio_list[1], '-vn',
                f'-filter_complex', 'acrossfade=d={transition_time}:c1=tri:c2=squ', temp1])
        for i in range(2, len(audio_list) - 1):
            subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', temp_file(i-1), '-i', audio_list[i], '-vn',
                f'-filter_complex', 'acrossfade=d={transition_time}:c1=tri:c2=squ', temp_file(i)])
        # final call to convert to mp3
        subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', temp_file(len(audio_list) - 2), '-i', audio_list[-1], '-vn',
            f'-filter_complex', 'acrossfade=d={transition_time}:c1=tri:c2=squ', output_path])
    elif len(audio_list) == 2:
        subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', audio_list[0], '-i', audio_list[1], '-vn',
            f'-filter_complex', 'acrossfade=d={transition_time}:c1=tri:c2=squ', output_path])
    elif len(audio_list) == 1:
        shutil.copyfile(audio_list[0], output_path)
    else:
        raise ValueError("Empty audio list")

    if not debugging:
        try:
            os.remove(temp0)
            os.remove(temp1)
        except OSError:
            pass
    
    return output_path

def extract_audio(video_file, time1, time2, output_file):
    """Creates audio file from video and timestamps"""
    subprocess.call(['ffmpeg', '-y', #'-hide_banner', '-loglevel', 'panic',
                    '-i', video_file,
                    '-ss', time1, '-to', time2, #f"volume=enable='between(t,t1,t2)':volume=0, volume=enable='between(t,t3,t4)':volume=0",
                    '-c:a', 'libmp3lame', output_file])

def merge_audio(audio_file1, audio_file2, output_file, vol1=1.0, vol2=1.0):
    """Merges two audios into one. option to adjust volumes for both audio"""
    subprocess.call(['ffmpeg', '-y', #'-hide_banner', '-loglevel', 'panic',
                    '-i', audio_file1, '-i', audio_file2, '-filter_complex',
                    f'[0:0]volume={vol1}[a];[1:0]volume={vol2}[b];[a][b]amix=inputs=2:duration=longest', '-c:a', 'libmp3lame', output_file])