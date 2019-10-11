import subprocess

def call_ffmpeg(command, overwrite=True, verbose=False):
    """Executes a ffmpeg command-line string"""
    command_list = ['ffmpeg']
    if not verbose:
        command_list.extend(['-hide_banner', '-loglevel', 'panic'])
    if overwrite:
        command_list.append('-y')
    command_list.extend(command.strip('ffmpeg').strip().split(' '))
    subprocess.call(command_list)

def call_external(command_list):
    """Opens external program and returns the output"""
    return subprocess.check_output(command_list).decode('utf-8').strip()

def get_duration(path):
    """Get duration of media"""
    return float(call_external(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path]))