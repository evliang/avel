import os
import shutil
import subprocess
from avel.shared_lib import call_ffmpeg, call_external, get_duration

def get_dimensions(path):
    """Get dimensions of a video"""
    dimensions = call_external(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x', path])
    # Ranma ½ video returns '576x432\r\n\r\n\r\n720x480'
    return tuple(map(int,dimensions.partition('\r\n')[0].split('x')))

def is_wide_video(path):
    (width, height) = get_dimensions(path)
    return width >= height * 1.1

def _get_framerate(path):
    """Gets the framerate of a video"""
    num,denom = list(map(int, call_external(['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', '0', '-show_entries', 'stream=r_frame_rate', path]).split('/')))
    return num*1.0/denom

def trim_video(inp, start_time, end_time, outp):
    """Trims a single video"""
    call_ffmpeg(f'ffmpeg -i {inp} -ss {start_time} -to {end_time} {outp}')

def create_image_video(image, seconds, output_filename):
    """creates video from single image. seconds determines length of video"""
    call_ffmpeg(f'ffmpeg -loop 1 -i {image} -c:v libx264 -t {seconds} -pix_fmt yuv420p -vf pad=ceil(iw/2)*2:ceil(ih/2)*2 {output_filename}')

# https://github.com/tanersener/ffmpeg-video-slideshow-scripts/tree/master/transition_scripts
def create_image_slideshow_fade(images, seconds, output_filename):
    """Creates a simple image slideshow with fade transition"""
    all_dimensions = list(map(lambda x: get_dimensions(x), images))
    width, height = max(map(lambda x: x, all_dimensions))
    part1 = []
    part2, part3 = '', ''
    if len(images) > 2:
        for (idx,i) in enumerate(images):
            part1 += (f'-loop 1 -t {seconds} -i'.split() + [i])
            if idx == 0:
                part2 += f'[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=out:st={seconds - 0.75}:d=1[v0];'
            else:
                part2 += f'[{idx}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st={seconds - 0.75}:d=1[v{idx}];'
            part3 += f'[v{idx}]'
        part3 += f'concat=n={len(images)}:v=1:a=0,format=yuv420p[v]'
    elif len(images) == 2:
        raise NotImplementedError() # todo. easiest to create two image videos and concat?
    elif len(images) == 1:
        create_image_video(images[0], seconds, output_filename)
    else:
        raise(ValueError("No images for slideshow"))
    call_ffmpeg(f'ffmpeg {part1} -filter_complex {part2 + part3} -map [v] {output_filename}')

def create_scrolling_image(image, seconds, direction, output_filename):
    """Creates horizontal video to scroll through a vertical image."""
    (width,height) = get_dimensions(image)
    adj_height = int(width*9.0/16)
    dimensions = str(width) + 'x' + str(adj_height) # horizontal dimensions
    speed = int((height - adj_height * 1.0)/seconds)

    if direction == 'zoomout':
        # subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-loop', '1', '-t', str(seconds), '-i', image, '-vf', '''"zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125"''', '-c:v', 'libx264', output_filename,  '-y'])
        call_ffmpeg(f'''ffmpeg -loop 1 -t {seconds} -i {image} -vf "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125" -c:v libx264 {output_filename}''')
    elif direction == 'zoomin':
        # subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-r', '25', '-i', image, '-filter_complex', "scale=-2:10*ih,zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',scale=-2:720", '-shortest', '-c:v', 'libx264', output_filename,  '-y'])
        (width, height) = get_dimensions(image)
        width = int(width * 0.25)
        height = int(height * 0.25)
        call_ffmpeg(f'''ffmpeg -loop 1 -t {seconds} -i {image} -vf zoompan=z='zoom+0.001:s={width}x{height} -c:v libx264 -preset fast {output_filename}''')
        #subprocess.call(['ffmpeg', '-loop', '1', '-i', image, '-vf', f"zoompan=z='zoom+0.001:s={width}x{height}", '-c:v', 'libx264', '-preset', 'fast', '-t', str(seconds), '-y', output_filename ])
    elif direction == "down":
        call_ffmpeg(f'''ffmpeg -loop 1 -t {seconds} -i {image} -filter_complex color=white:s={dimensions}[bg];[bg][0]overlay=y=-'t*{speed}':shortest=1[video] -r 25/1 -preset ultrafast -map [video] {output_filename}''')
        #subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-loop', '1', '-t', str(seconds), '-i', image, '-filter_complex', 'color=white:s=' + dimensions + "[bg];[bg][0]overlay=y=-'t*" + str(speed) + "':shortest=1[video]", '-r', '25/1', '-preset', 'ultrafast', '-map', '[video]', output_filename,  '-y'])
    else:
        # going up:
        call_ffmpeg(f'''ffmpeg -loop 1 -t {seconds} -i {image} -filter_complex color=white:s={dimensions}[bg];[bg][0]overlay=y=main_h-overlay_h+'t*{speed}':shortest=1[video] -r 25/1 -preset ultrafast -map [video] {output_filename}''')
        #subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-loop', '1', '-t', str(seconds), '-i', image, '-filter_complex', 'color=white:s=' + dimensions + "[bg];[bg][0]overlay=y=main_h-overlay_h+'t*" + str(speed) + "':shortest=1[video]", '-r', '25/1', '-preset', 'ultrafast', '-map', '[video]', output_filename, '-y'])

def slowmo(input_vid, output_path, multiplier=2.0, duration=None):
    if duration:
        video_dur = get_duration(input_vid)
        if duration > video_dur:
            call_ffmpeg(f'ffmpeg -i {input_vid} -filter:v setpts= {duration*1.0/video_dur} *PTS {output_path}')
            #subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-i', input_vid, '-filter:v', 'setpts=' + str(duration*1.0/video_dur) + '*PTS', output_path, '-y'])
        else:
            shutil.copyfile(input_vid, output_path)
    else:
        call_ffmpeg(f'ffmpeg -i {input_vid} -filter:v setpts= {multiplier} *PTS {output_path}')
        #subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-i', input_vid, '-filter:v', 'setpts=' + str(multiplier) + '*PTS', output_path, '-y'])

def combine_videos(files, output_filename, debugging=False):
    """Concatting video files of all dimensions and durations together"""
    def intermediate_file(idx):
        return 'intermediate' + str(idx) + '.ts'

    if (len(files) < 400):
        for (idx, f) in enumerate(files):
            call_ffmpeg(f'ffmpeg -i {f} -c copy -bsf:v h264_mp4toannexb -f mpegts {intermediate_file(idx)}')
        call_ffmpeg(f"ffmpeg -i concat:{'|'.join(map(lambda x: intermediate_file(x), range(0,len(files)) ))} -c copy {output_filename}")
        #subprocess.call(['ffmpeg', '-y', '-i', 'concat:' + '|'.join(map(lambda x: intermediate_file(x), range(0,len(files)) )), '-c', 'copy', output_filename])

        if not debugging:
            for (idx, _) in enumerate(files):
                os.remove(intermediate_file(idx))
    else:
        # there was an issue with concatting over 418 files: "The command is is too long."
        with open('templist.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(map(lambda x: "file '" + x + "'", files)))
        # this seems to work as well, but I get a lot of warning-like messages:
        # os.system('ffmpeg -hide_banner -loglevel panic -f concat -safe 0 -i templist.txt -codec copy ' + output_filename)
        call_ffmpeg(f'ffmpeg -i templist.txt -f concat -safe 0 -codec copy {output_filename}')

def blur_video(filePath, output_filename, resolution=None, debugging=False):
    """Creates a video with blurred sides (for clips that are not the same width as the final video's width.
    This option works well for now, but takes the resolution from the first video"""
    call_ffmpeg(f'ffmpeg -i {filePath} -filter_complex ' + r"[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop='if(gte(dar,16/9),ih*16/9,iw)':'if(gte(dar,16/9),ih,iw*9/16)' " + output_filename)
    if not debugging:
        os.remove(filePath)
    return output_filename

def combine_audio_video(audioPath, videoPath, output_filename, debugging=False):
    """Combining audio and video into one video file. Shorter duration of video/audio determines the final video's duration"""
    call_ffmpeg(f'ffmpeg -i {audioPath} -i {videoPath} -codec copy -shortest {output_filename}')

    if not debugging:
        os.remove(audioPath)
        os.remove(videoPath)
    return output_filename