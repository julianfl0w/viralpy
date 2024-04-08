import subprocess

import subprocess

def remove_segment_from_video(input_file, output_file, start_time, end_time):
    """
    Removes a segment from a video file and ensures audio is synchronized.

    Args:
    input_file (str): Path to the input video file.
    output_file (str): Path to the output video file, with the segment removed.
    start_time (int or float): Start time of the segment to remove, in seconds.
    end_time (int or float): End time of the segment to remove, in seconds.
    """
    # Construct the FFmpeg command to trim both video and audio
    command = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex',
        f'[0:v]trim=start=0:end={start_time},setpts=PTS-STARTPTS[firstv];' + 
        f'[0:v]trim=start={end_time},setpts=PTS-STARTPTS[secondv];' + 
        f'[0:a]atrim=start=0:end={start_time},asetpts=PTS-STARTPTS[firsta];' + 
        f'[0:a]atrim=start={end_time},asetpts=PTS-STARTPTS[seconda];' + 
        '[firstv][secondv]concat=n=2:v=1:a=0[video];' + 
        '[firsta][seconda]concat=n=2:v=0:a=1[audio]',
        '-map', '[video]',
        '-map', '[audio]',
        output_file
    ]

    # Execute the command
    subprocess.run(command, check=True)

import sys
# Example usage
input_video = sys.argv[1]
output_video = input_video[:-4] + "_trim.mp4"
remove_segment_from_video(input_video, output_video, 26.2, 27.3)
