import subprocess
import os

def extract_audio(input_dir):
    # Ensure the input directory exists
    if not os.path.isdir(input_dir):
        print(f"The directory {input_dir} does not exist.")
        return
    
    # Iterate over every file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith("_edited.mp4"):
            continue
        if filename.endswith(".mp4"):
            # Construct the full path to the input file
            input_file_path = os.path.join(input_dir, filename)
            
            # Construct the output file path (change extension to .m4a or .mp3 as needed)
            output_file_path = os.path.join(input_dir, os.path.splitext(filename)[0] + ".m4a")
            if os.path.exists(output_file_path):
                continue

            # Construct the FFmpeg command
            ffmpeg_command = [
                "ffmpeg",
                "-i", input_file_path,  # Input file
                "-vn",  # No video
                "-acodec", "copy",  # Copy the audio stream without re-encoding
                output_file_path  # Output file
            ]
            
            # Execute the FFmpeg command
            try:
                subprocess.run(ffmpeg_command, check=True)
                print(f"Extracted audio to {output_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to extract audio from {input_file_path}: {e}")

    for filename in os.listdir(input_dir):
        if filename.endswith(".mp4"):
            # Construct the full path to the input file
            input_file_path = os.path.join(input_dir, filename)

            # Construct the expected MP3 file name and its full path
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            input_mp3_path = os.path.join(input_dir, mp3_filename)
            
            # Check if the corresponding MP3 file exists
            if not os.path.exists(input_mp3_path):
                continue
            
            # Construct the output file path
            output_file_path = os.path.join(input_dir, os.path.splitext(filename)[0] + "_edited.mp4")
            if os.path.exists(output_file_path):
                continue
            
            #ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
            # Construct the FFmpeg command to combine video and audio
            ffmpeg_command = [
                "ffmpeg",
                "-i", input_file_path,  # Input MP4 file
                "-i", input_mp3_path,  # Input MP3 file
                "-c:v", "copy",  # Copy the video stream as is
                "-c:a", "aac",  # Re-encode audio to ensure compatibility
                "-map", "0:v:0",
                "-map", "1:a:0",
                output_file_path  # Output file
            ]
            print(f"Running {' '.join(ffmpeg_command)}")
            
            # Execute the FFmpeg command
            try:
                subprocess.run(ffmpeg_command, check=True)
                print(f"Combined video and audio into {output_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to combine files {input_file_path} and {input_mp3_path}: {e}")

import sys
# Example usage
# Replace 'your_directory_path_here' with the path to the directory containing your MP4 files
extract_audio(sys.argv[1])

