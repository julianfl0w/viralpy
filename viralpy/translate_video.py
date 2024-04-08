from . import extract_audio
from . import translate_audio

import sys

def translateVideo(filename):
    audioFilename = extract_audio.extractAudio(filename)
    print(audioFilename)
    translatedCaptions = translate_audio.translateAudio(audioFilename)
if __name__ == "__main__":
    translateVideo(sys.argv[1])