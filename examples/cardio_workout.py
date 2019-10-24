import os
from avel.video_lib import drawtext, create_drawtext_dict

def get_countdown_str(seconds):
    return r'%{eif:trunc(mod(' + str(seconds) + r'-t\,60)):d:2}'

def create_hiit_overlays(initial_time, hi_time, low_time, num_sets):
    # jump rope, jumping jacks, squats, jumping squats, sprint in place, push ups
    hiit_overlay = []
    for i in range(num_sets):
        t1 = initial_time + i*(hi_time+low_time)
        t2 = t1 + hi_time
        hiit_overlay.append(
            create_drawtext_dict("JUMPING JACKS", "mid_x", "top", 90, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1},{t1 + 5})" ))
        hiit_overlay.append(
            create_drawtext_dict(get_countdown_str(hi_time), "right", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t1},{t2})" ))

        hiit_overlay.append(
            create_drawtext_dict("rest", "mid_x", "top", 75,
                enable=f"between(t,{t2},{t2 + 5})"))
        hiit_overlay.append(
            create_drawtext_dict("rest " + get_countdown_str(hi_time), "right", "top", 75, box='1:boxcolor=black@0.5:boxborderw=5:',
                enable=f"between(t,{t2},{t2 + low_time})" ))
    return hiit_overlay

def draw_exercise_overlay(input_video, output_dir=None):
    warmup_time, cooldown_time = 4 * 60, 2 * 60
    hi_time, low_time = 15, 45
    exercise_time = 15 * 60

    overlay = [
        create_drawtext_dict("warmup your heart", "mid_x", "top", 40, enable=f"between(t,0,{warmup_time - 5})"),
        create_drawtext_dict("GET READY", "mid_x", "mid_y", 80, enable=f"between(t,{warmup_time - 5},{warmup_time})") ]
    overlay.extend(create_hiit_overlays(warmup_time, hi_time, low_time, exercise_time // (hi_time + low_time)))
    # burn mode
    overlay.append(create_drawtext_dict("cool down!!", "mid_x", "mid_y", 80, enable=f"between(t,{warmup_time + exercise_time},{warmup_time + exercise_time + cooldown_time})"))

    f,_,ext = os.path.basename(input_video).rpartition('.')
    new_filename = f"{f}_new.{ext}"
    output_dir = os.path.dirname(input_video) if output_dir is None else output_dir
    output_video = os.path.join(output_dir, new_filename)
    drawtext(input_video, output_video, overlay)
    return output_video

if __name__ == '__main__':
    draw_exercise_overlay("D:\\TV\\Hunter X Hunter 2011\\Season 2\\Hunter.X.Hunter.2011.S02E58.mkv", "D:\\workout_vids\\")