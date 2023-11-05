import cv2
from gaze_tracking import GazeTracking
from time import perf_counter
from os import walk
from random import randint

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

mypath = r'logo'
filenames = list(walk(mypath))[0][2]
logos_time = [0] * len(filenames)
time_old = perf_counter()
photos_shows = []

for i in range(5):
    r1 = randint(0, len(filenames))
    r2 = randint(0, len(filenames))
    while True:
        if r1 not in photos_shows:
            photos_shows.append(r1)
            break
        r1 = randint(0, len(filenames))
    while True:
        if r2 not in photos_shows:
            photos_shows.append(r2)
            break
        r2 = randint(0, len(filenames))

    image1 = cv2.imread(filenames[r1])
    image2 = cv2.imread(filenames[r2])
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)
        frame = gaze.annotated_frame()

        pos = gaze.horizontal_ratio()
        print(pos)

        if pos is None:
            # "Blinking"
            pass
        elif pos <= 0.6:
            # "Looking right"
            logos_time[r2] += perf_counter() - time_old
            time_old = perf_counter()
        elif pos > 0.6:
            # "Looking left"
            logos_time[r1] += perf_counter() - time_old
            time_old = perf_counter()

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        cv2.namedWindow("programs", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("programs", 1680, 1000)
        cv2.imshow("programs", frame)

        if cv2.waitKey(1) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()
