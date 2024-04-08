import sys
import json
import os
import cv2
from . import extractAudio
from . import translate_audio

def oneword(videofile, offset = 0.1, y_depth=None):

    for path in os.listdir("."):
        if path.endswith(".mp3") or path.endswith(".m4a"):
            audiofile = path

    translate_audio.translateAudio(audiofile)

    # print the result
    #print(json.dumps(result, indent = 2, ensure_ascii = False))

    print("opening videofile")
    # open the videofile
    output_file = videofile + "_silent_sub.mp4"

    # Open the input video file
    cap = cv2.VideoCapture(videofile)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")


    if y_depth is None:
        y_depth = height/2 + 100

    # Create the output video file
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # describe the type of font
    # to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX


    # Window name in which image is displayed
    window_name = 'Image'

    import numpy as np

    i = 0

    # Read frames from input video and write them to output video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("frame " + str(i))
            lastWord = ""
            
            capture_time_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 + offset

            for segment in result["segments"]:
                for word in segment["words"]:
                    if capture_time_sec >= word["start"] and capture_time_sec < word["end"]:

                        # Use putText() method for
                        # inserting text on video
                        #print(frame.shape)
                        if word != lastWord:
                            emptyFrame = np.zeros(frame.shape)

                            # get boundary of this text
                            textsize = cv2.getTextSize(word["text"], fontFace = font, fontScale = 4, thickness=7)[0]
                            

                            # get coords based on boundary
                            textX = int((emptyFrame.shape[1] - textsize[0]) / 2)
                            textY = int((emptyFrame.shape[0] + textsize[1]) / 2)
                            textY = int(y_depth)
                        
                            cv2.putText(img = emptyFrame,
                                    text = word["text"],
                                    org = (textX, textY),
                                    fontFace = font, fontScale = 4,
                                    color = (255, 255, 255),
                                    thickness = 7,
                                    lineType = cv2.LINE_4)

                            # Taking a matrix of size 5 as the kernel
                            ks = 12
                            kernel = np.ones((ks, ks))/(ks**2)

                            alpha = cv2.dilate(emptyFrame, kernel, iterations=1)[:,:,:1]/255.0

                        frame_with_gap = np.multiply(frame, 1.0-alpha)/255.0
                        text_with_gap = np.multiply(emptyFrame, alpha)/255.0
                        frame = frame_with_gap + text_with_gap
                        frame = (frame*255).astype(np.uint8)

                        #print(np.min(alpha))
                        # Displaying the image
                        #cv2.imshow(window_name, final_image) 
                        #cv2.waitKey(1)
                    lastWord = word
                    
            out.write(frame)
            i+=1
            #if i > 60:
            #    break
        else:
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # combine video with audio file
    finaloutput = videofile + "_subs.mp4"
    #os.system("ffmpeg -i " + output_file + " -i " + audiofile + " -c copy " + finaloutput)
    os.system("ffmpeg -i " + output_file + " -i " + audiofile + " " + finaloutput)

if __name__ == "__main__":
    oneword(sys.argv[1])
