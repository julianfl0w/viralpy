import os,sys,json

def transcribeAudio(audioFilename, language = 'ar'):
    transcriptJson = audioFilename + ".json"
    # generate per-word timeslices
    if not os.path.exists(transcriptJson):
        print("generating subtitle")    
        #import whisper_timestamped as whisper
        import whisper
        audio = whisper.load_audio(audioFilename)
        model = whisper.load_model("small")
        transcriptDict = whisper.transcribe(model, audio, language=language)
        with open(transcriptJson, 'w+') as rf:
            rf.write(json.dumps(transcriptDict, indent=2))
        
    # or open them if they exist
    else:
        print("...from file")
        with open(transcriptJson, 'r') as rf:
            transcriptDict = json.loads(rf.read())
    return transcriptDict

def translateAudio(audioFilename, language = 'ar'):

    transcriptDict = transcribeAudio(audioFilename,language)
    for sentence in transcriptDict["segments"]:
        print(sentence["text"])