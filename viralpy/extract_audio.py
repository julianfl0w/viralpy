import subprocess
import os

def combine_video_and_audio(filename):

    # Construct the expected MP3 file name and its full path
    mp3_filename = os.path.splitext(filename)[0] + ".mp3"
    filename_mp3 = mp3_filename
    
    # Check if the corresponding MP3 file exists
    if not os.path.exists(filename_mp3):
        return
    
    # Construct the output file path
    combined_filename = os.path.splitext(filename)[0] + "_edited.mp4"
    if os.path.exists(combined_filename):
        return
    
    #ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
    # Construct the FFmpeg command to combine video and audio
    ffmpeg_command = [
        "ffmpeg",
        "-i", filename,  # Input MP4 file
        "-i", filename_mp3,  # Input MP3 file
        "-c:v", "copy",  # Copy the video stream as is
        "-c:a", "aac",  # Re-encode audio to ensure compatibility
        "-map", "0:v:0",
        "-map", "1:a:0",
        combined_filename  # Output file
    ]
    print(f"Running {' '.join(ffmpeg_command)}")
    
    # Execute the FFmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Combined video and audio into {combined_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to combine files {filename} and {filename_mp3}: {e}")


def extractAudioFromVideo(videoFilename, touchup = False):
    if videoFilename.endswith("_edited.mp4"):
        return
    if videoFilename.endswith(".mp4"):
        print(f"extracting audio from {videoFilename}")
          # Construct the output file path (change extension to .m4a or .mp3 as needed)
        audioFilename = os.path.splitext(videoFilename)[0] + ".m4a"
        if os.path.exists(audioFilename):
            return audioFilename

        if touchup:
            print("exporting audio touchup")

            # Normalize the audio to -1dB and compress it with a ratio of 4:1
            processCmd ='-af "compand=attacks=1:decays=1:points=-80/-80|-20.0/-6.0|0/-3.0:soft-knee=6:gain=3,highpass=f=200,lowpass=f=3000,loudnorm=I=-16:LRA=11:TP=-1.5"'
            processCmd = ''
            cmd = "ffmpeg -i " + videoFilename + " " + processCmd + " " + audioFilename
            print(cmd)
            os.system(cmd)
            return audioFilename

        # Construct the FFmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i", videoFilename,  # Input file
            "-vn",  # No video
            "-acodec", "copy",  # Copy the audio stream without re-encoding
            audioFilename  # Output file
        ]
        
        # Execute the FFmpeg command
        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"Extracted audio to {audioFilename}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract audio from {videoFilename}: {e}")
        return audioFilename

def extractAudioTouchup(videofile):
    print("exporting audio")
    # export video as audio only
    if not os.path.exists(audiofile):

        # Normalize the audio to -1dB and compress it with a ratio of 4:1
        processCmd ='-af "compand=attacks=1:decays=1:points=-80/-80|-20.0/-6.0|0/-3.0:soft-knee=6:gain=3,highpass=f=200,lowpass=f=3000,loudnorm=I=-16:LRA=11:TP=-1.5"'
        processCmd = ''
        cmd = "ffmpeg -i " + videofile + " " + processCmd + " " + audiofile
        print(cmd)
        os.system(cmd)


def extractAudio(input_dir, touchup=False):
    # Ensure the input directory exists
    if os.path.isfile(input_dir):
        return extractAudioFromVideo(input_dir,touchup=touchup)
    
    # Iterate over every file in the input directory
    for filename in os.listdir(input_dir):
        extractAudioFromVideo(os.path.join(input_dir,filename), touchup=touchup)
    #for filename in os.listdir(input_dir):
        if filename.endswith(".mp4"):
            combine_video_and_audio(os.path.join(input_dir, filename))
import sys
# Example usage
# Replace 'your_directory_path_here' with the path to the directory containing your MP4 files
if __name__ == "__main__":
    extract_audio(sys.argv[1])

