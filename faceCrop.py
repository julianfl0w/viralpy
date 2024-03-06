import cv2
import numpy as np
import json
import face_recognition

import os


def generateLocations(video_path, faceImages, fx=0.25, fy=0.25):
    outpath = video_path[:-3] + "_faces.json"
    if os.path.exists(outpath):
        with open(outpath, "r") as f:
            return json.loads(f.read())

    outlist = []
    # Load the video
    cap = cv2.VideoCapture(video_path)

    known_face_encodings = []
    known_face_names = []

    for faceImage in faceImages:
        # Load a sample picture and learn how to recognize it.
        loadedFaceImage = face_recognition.load_image_file(faceImage)
        david_face_encoding = face_recognition.face_encodings(loadedFaceImage)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings += [david_face_encoding]
        known_face_names += [
            faceImage,
        ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    frameNo = 0

    while True:
        print(frameNo)
        # Grab a single frame of video
        ret, sourceFrame = cap.read()

        if not ret:
            break

        thisFrameDict= {}

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(sourceFrame, (0, 0), fx=fx, fy=fy)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top /= fy
            right /= fx
            bottom /= fy
            left /= fx

            thisFrameDict[name] = {
                "top": top,
                "bottom": bottom,
                "left": left,
                "right": right,
                "center_x": (left + right) // 2,
                "center_y": (top + bottom) // 2,
            }
        outlist += [thisFrameDict]
        frameNo += 1

    with open(outpath, "w+") as f:
        f.write(json.dumps(outlist, indent=2))

    # Release handle to the webcam
    cap.release()
    return outlist


def updateCenters(faces, startCenterX, startCenterY, frame_count, updateAlpha=0.2):
    center_x = startCenterX
    center_y = startCenterY
    centerList = [None] * frame_count
    
    for frameNo, faceDict in enumerate(faces):
        for name, loc in faceDict.items():
            if name == "Unknown":
                continue
            center_x = (loc["center_x"] * updateAlpha) + (
                center_x * (1 - updateAlpha)
            )
            center_y = (loc["center_y"] * updateAlpha) + (
                center_y * (1 - updateAlpha)
            )
            print(center_x)
        centerList[frameNo] = [center_x, center_y]

    print(centerList)
    return centerList


def cropToCenter(sourceFrame, destShape, centerx, centery):
    sourceHeight, sourceWidth = sourceFrame.shape[:2]
    destWidth, destHeight = destShape[:2]
    destAspectRatio = destWidth / destHeight
    sourceAspectRatio = sourceWidth / sourceHeight

    # Determine the largest area of the source that fits the destination aspect ratio
    if destAspectRatio > sourceAspectRatio:
        # Destination is wider than the source
        cropWidth = sourceWidth
        cropHeight = int(cropWidth / destAspectRatio)
    else:
        # Destination is taller than the source
        cropHeight = sourceHeight
        cropWidth = int(cropHeight * destAspectRatio)

    # Calculate the top-left corner of the cropped area, ensuring it's centered
    cropX = max(0, min(sourceWidth - cropWidth, int(centerx - cropWidth / 2)))
    cropY = max(0, min(sourceHeight - cropHeight, int(centery - cropHeight / 2)))

    # Crop the source image
    cropped_img = sourceFrame[cropY : cropY + cropHeight, cropX : cropX + cropWidth]

    # Resize the cropped image to the destination size
    resized_img = cv2.resize(
        cropped_img, (destWidth, destHeight), interpolation=cv2.INTER_LINEAR
    )

    return resized_img


class FaceCrop:

    def __init__(self, video_path, faceImages, rate = 0.02, testing=False):
        
        outpath = video_path[:-3] + "_zoom.mp4"
        # Load the video
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        sourceWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        sourceHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        # Get the total number of frames in the video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        faces = generateLocations(video_path, faceImages=faceImages)
        centersArray = updateCenters(
            faces, sourceWidth / 2, sourceHeight / 2, frame_count=frame_count,
            updateAlpha=rate
        )
        with open("tmp.json", "w+") as f:
            f.write(json.dumps(centersArray, indent=2))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        destWidth = 1080
        destHeight = 1920

        # Create the output video file
        out = cv2.VideoWriter(outpath, fourcc, fps, (destWidth, destHeight))
        frameNo = 0

        while True:
            # Grab a single frame of video
            ret, sourceFrame = cap.read()
            print(frameNo)

            if not ret:
                print("DONE")
                break

            destFrame = sourceFrame
            if testing:
                destFrame = cv2.circle(
                    sourceFrame,
                    (
                        int(centersArray[frameNo][0]),
                        int(centersArray[frameNo][1]),
                    ),
                    radius=100,
                    color=(255, 0, 0),
                    thickness=20,
                )
                destFrame = cv2.resize(destFrame, (destWidth, destHeight))
            else:
                destFrame = cropToCenter(sourceFrame=sourceFrame, destShape=(destWidth, destHeight), centerx=centersArray[frameNo][0], centery=int(centersArray[frameNo][1]))
            #
            # Display the resulting image
            out.write(destFrame)
            frameNo += 1

        # Release handle to the webcam
        cap.release()


import sys

if __name__ == "__main__":

    FaceCrop(sys.argv[1], [sys.argv[2]], float(sys.argv[3]))
