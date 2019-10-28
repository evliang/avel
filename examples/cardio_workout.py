import os
import random
from avel.video_lib import drawtext, create_drawtext_dict

"""
create_hiit_video takes in a video file (e.g. TV show) and outputs a HIIT workout video
It employs a routine of 15s of high-intensity exercises, followed by 45s of low-intensity
It displays text to inform me when to work out and rest
todo: mix in EDM music in the background, with louder volume for high-intensity portion
"""

def get_countdown_str(seconds):
    return r'%{eif\:trunc(mod(' + str(seconds) + r'-t\,60))\:d\:2}'

def get_rand_exercise():
    return random.choice(["jump rope", "jumping jacks", "squats", "jumping squats", "sprint in place", "push ups"])

def create_hiit_overlays(initial_time, hi_time, low_time, num_sets):
    """
    Creates a list of overlay dictionaries
    fontsize is hardcoded for 720p video resolution
    """
    hiit_overlay = []
    exercise = get_rand_exercise()
    for i in range(num_sets):
        t1 = initial_time + i*(hi_time+low_time)
        hiit_overlay.append(
            create_drawtext_dict(exercise.capitalize(), "mid_x", "top", 90, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1},{t1 + hi_time})" ))
        hiit_overlay.append(
            create_drawtext_dict(get_countdown_str(t1 + hi_time), "right", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1},{t1 + hi_time})" ))

        hiit_overlay.append(
            create_drawtext_dict("rest", "mid_x", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1 + hi_time},{t1 + hi_time + 5})"))
        hiit_overlay.append(
            create_drawtext_dict("rest " + get_countdown_str(t1 + hi_time + low_time), "right", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1 + hi_time + 5},{t1 + hi_time + low_time - 5})" ))
        exercise = get_rand_exercise()
        hiit_overlay.append(
            create_drawtext_dict(f"next is {exercise} {get_countdown_str(t1 + hi_time + low_time)}", "right", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1 + hi_time + low_time - 5},{t1 + hi_time + low_time})" ))
    return hiit_overlay

def create_hiit_video(input_video, output_dir=None):
    warmup_time, cooldown_time = 4 * 60, 2 * 60
    hi_time, low_time = 15, 45
    exercise_time = 15 * 60

    overlay = [
        create_drawtext_dict("warmup", "mid_x", "top", 50, enable=f"between(t,0,{warmup_time - 5})", box='1:boxcolor=black@0.5:boxborderw=5:'),
        create_drawtext_dict("GET READY", "mid_x", "mid_y", 100, enable=f"between(t,{warmup_time - 5},{warmup_time})", box='1:boxcolor=black@0.5:boxborderw=5:') ]
    
    overlay.extend(create_hiit_overlays(warmup_time, hi_time, low_time, exercise_time // (hi_time + low_time)))
    # burn mode
    overlay.append(create_drawtext_dict("cool down!", "mid_x", "mid_y", 80, enable=f"between(t,{warmup_time + exercise_time},{warmup_time + exercise_time + cooldown_time})"))

    f,_,ext = os.path.basename(input_video).rpartition('.')
    new_filename = f"{f}_cardio.{ext}"
    output_dir = os.path.dirname(input_video) if output_dir is None else output_dir
    output_video = os.path.join(output_dir, new_filename)
    drawtext(input_video, output_video, overlay)
    return output_video

if __name__ == '__main__':
    create_hiit_video("D:\\TV\\Hunter X Hunter 2011\\Season 2\\Hunter.X.Hunter.2011.S02E58.mkv", "D:\\workout_vids\\")