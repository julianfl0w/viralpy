#y2mate.is - Farmacia de guardia 1x27-4fYF2807anc-480pp-1705346874.mp4
import subprocess
import os
import json
#import whisper
import whisper_timestamped as whisper
import sys

from transformers import pipeline

def removeUhhs(data):
    """ Create an SRT file from OpenAI Whisper data """
    srt_content = {}
    for i, segment in enumerate(data['segments']):
        srt_content[segment] = deo
        for j, word in enumerate(segment['words']):
            pass

    return srt_content

def generate(infilename = "input.mp4"):
    basename = infilename[:-4]
    mp3filename = f"{basename}.mp3"
    if not os.path.exists(mp3filename):
        # Command to extract audio from a video file using ffmpeg
        command = f"ffmpeg -i {infilename} -q:a 0 -map a {mp3filename}"
        # Execute the command
        subprocess.run(command, shell=True)

    transcriptionFilename = f"{basename}.json"
    if not os.path.exists(transcriptionFilename):
        model = whisper.load_model("base")
        transcription = whisper.transcribe(model, mp3filename, language="en", detect_disfluencies=True)
        with open(transcriptionFilename, 'w+') as f:
            f.write(json.dumps(transcription, indent=2))

    moddedTranscript = f"{basename}_modded.json"
    if not os.path.exists(moddedTranscript):
        with open(transcriptionFilename, 'r') as f:
            whisper_data = json.loads(f.read())

        srt_content = removeUhhs(whisper_data)

        # Write to a file
        with open(moddedTranscript, "w") as file:
            file.write(json.dumps(srt_content))

generate(sys.argv[1])