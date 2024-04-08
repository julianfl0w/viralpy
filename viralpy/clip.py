import subprocess
import os
import sys

def extract_video_segment(input_file, start_time, end_time, clipName):
    # Create a directory with the same name as the output file, without the extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(os.path.dirname(input_file), clipName)
    os.makedirs(output_dir, exist_ok=True)

    # Construct the output file path
    output_file = os.path.join(output_dir, clipName + ".mp4")

    # Convert start and end times to seconds
    start_seconds = sum(x * float(t) for x, t in zip([3600, 60, 1], start_time.split(":")))
    end_seconds = sum(x * float(t) for x, t in zip([3600, 60, 1], end_time.split(":")))
    # Calculate duration
    duration_seconds = end_seconds - start_seconds

    command = [
        'ffmpeg',
        '-ss', str(start_seconds),  # Start time in seconds
        '-t', str(duration_seconds),  # Duration in seconds
        '-i', input_file,  # Input file
        '-c:v', 'copy',  # Copy the video stream
        '-c:a', 'copy',  # Copy the audio stream
        output_file  # Output file
    ]

    # Execute the FFmpeg command
    subprocess.run(command, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_video> <start_time> <end_time>")
        sys.exit(1)
    
    input_video = sys.argv[1]
    start_time = sys.argv[2]  # ex "00:26:12"
    end_time = sys.argv[3]    # ex "00:26:34"
    clipName = sys.argv[4]
    extract_video_segment(input_video, start_time, end_time, clipName)
