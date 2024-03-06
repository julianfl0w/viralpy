#y2mate.is - Farmacia de guardia 1x27-4fYF2807anc-480pp-1705346874.mp4
import subprocess
import os
import json
import whisper

from transformers import pipeline

# Specify the model to use
model_name = "Helsinki-NLP/opus-mt-es-en"

# Load the translation pipeline with the specified model
translator = pipeline("translation", model=model_name)


def convert_time(time_in_seconds):
    """ Convert time in seconds to SRT time format """
    millisec = int((time_in_seconds % 1) * 1000)
    seconds = int(time_in_seconds) % 60
    minutes = (int(time_in_seconds) // 60) % 60
    hours = (int(time_in_seconds) // 3600)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def create_srt_from_whisper(data):
    """ Create an SRT file from OpenAI Whisper data """
    srt_content = ""
    for i, segment in enumerate(data['segments']):
        for j, word in enumerate(segment['words']):
            start_time = convert_time(word['start'])
            end_time = convert_time(word['end'])

            translated_text = translator(word['word'])[0]['translation_text']
            print(translated_text)
            text = word['word'] + '\n' + translated_text
            srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"

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
        with open(transcriptionFilename, 'w+') as f:
            transcription = model.transcribe(mp3filename, language="es", word_timestamps=True)
            f.write(json.dumps(transcription, indent=2))

    srtFilename = f"{basename}.srt"
    if not os.path.exists(srtFilename):
        
        with open(transcriptionFilename, 'r') as f:
            whisper_data = json.loads(f.read())

        srt_content = create_srt_from_whisper(whisper_data)

        # Write to a file
        with open(srtFilename, "w") as file:
            file.write(srt_content)

generate()