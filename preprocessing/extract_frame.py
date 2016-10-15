# The simple implentation of obtaining the key frames of an original video clip.

# Input: an original video file.
# Output: multiple key frames (images).
#   Please note that, 1. different videos can have different key frames (images).
#                     2. you need to select a suitable and reasonable way to
#                        deal with the multiple output (frames, images) to represent the video.

import cv2, os, sys
import numpy as np
import preprocess_utility.pp_util as util


# The implementation of fetching the key frames.
def getKeyFrames(vidcap, store_frame_path):
    count = 0
    lastHist = None
    sumDiff = []
    n_frames = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    while vidcap.isOpened():
        success, frame = vidcap.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

        if count >0:
            diff = np.abs(hist - lastHist)
            s = np.sum(diff)
            sumDiff.append(s)
        lastHist = hist
        count += 1

    m = np.mean(sumDiff)
    std = np.std(sumDiff)

    candidates = []
    candidates_value = []
    for i in range(len(sumDiff)):
        if sumDiff[i] > m + std*3:
            candidates.append(i+1)
            candidates_value.append(sumDiff[i])
            

    if len(candidates) > 20:
        top10list = sorted(range(len(candidates_value)), key=lambda i: candidates_value[i])[-9:]
        res = []
        for i in top10list:
            res.append(candidates[i])
        candidates = sorted(res)

    candidates = [0] + candidates

    keyframes = []
    lastframe = -2
    for frame in candidates:
        if not frame == lastframe + 1:
            keyframes.append(frame)
        lastframe = frame

    count = 0
    for frame in keyframes:
        vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame)
        success, image = vidcap.read()
        jpg_name = store_frame_path+"frame"+str(count)+".jpg"   
        cv2.imwrite(jpg_name, image)
        
        if (os.path.getsize(jpg_name) > 0):
            count += 1
        else:
            # delete file
            os.remove(jpg_name)
        
        print "keyframe: " + str(frame)

    return keyframes

# single frame extraction
def frameExtract(input_store_path, search_path):
    video_file = search_path
    vidcap = cv2.VideoCapture(video_file)
    video_name = os.path.basename(video_file)
    store_frame_path = input_store_path + "/" + video_name[:-4]+"-" 
    keyframes = getKeyFrames(vidcap=vidcap, store_frame_path=store_frame_path)
    vidcap.release()

    return keyframes

# batch frame extraction
def batchFrameExtract(input_store_path, database_path):
    mp4_paths = util.get_mp4_paths(database_path)

    for path in mp4_paths:
        # 1. Set the access path to the original video clip.
        video_file = path

        # 2. Open the video clip.
        vidcap = cv2.VideoCapture(video_file)

        # 3. Get and store the resulting frames via the specific path.
        video_name = os.path.basename(video_file)
        folder_path = input_store_path + "/" + video_name[:-4]
        if (not os.path.exists(folder_path)):
            os.makedirs(folder_path)

        store_frame_path = folder_path+"/"+os.path.basename(video_file)[:-4]+"-"

        keyframes = getKeyFrames(vidcap=vidcap, store_frame_path=store_frame_path)
        
        # 4. Close the video clip.
        vidcap.release()
        folder_path = ""

# arg[1] = storage path
# arg[2] = database path

if __name__ == '__main__':
   
    if (len(sys.argv) != 3):
        print "Please input storage path directory for wav files or the video source path"
    elif (not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2])):
        print "Please input a valid storage path directory for wav files and/or video source path"
    else:
        input_store_path = sys.argv[1]
        path = sys.argv[2]

        #video_file = "/Users/Brandon/Documents/CS2108-Vine-Dataset/vine/training/1000046931730481152.mp4"
        #vidcap = cv2.VideoCapture(video_file)
        #store_frame_path = input_store_path+video_file[:-4]+"-"
        #keyframes = getKeyFrames(vidcap=vidcap, store_frame_path=store_frame_path)

        batchFrameExtract(input_store_path, path)
        
       