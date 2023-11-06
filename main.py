import cv2
from gaze_tracking import GazeTracking
from time import perf_counter
from os import walk
from random import randint
import numpy as np

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

time_to_show = 10  # sec

dir_path = r'logo_new_scaled'
filenames = list(walk(dir_path))[0][2]
print(filenames)
logos_time = [0] * len(filenames)
logos_already_shows = []
logos_pair = []

for round in range(5):
    r1 = 0
    r2 = 0
    for i in range(len(filenames)//2):
        r1 = randint(0, len(filenames)-1)
        r2 = randint(0, len(filenames)-1)
        while True:
            if r1 not in logos_already_shows:
                logos_already_shows.append(r1)
                break
            r1 = randint(0, len(filenames)-1)

        while True:
            if r2 not in logos_already_shows:
                logos_already_shows.append(r2)
                break
            r2 = randint(0, len(filenames)-1)

        logos_pair.append((r1, r2))
        print(r1, r2)
        image1 = cv2.imread(f'{dir_path}/{filenames[r1]}')
        image2 = cv2.imread(f'{dir_path}/{filenames[r2]}')

        time_start_10_sec = perf_counter()
        while perf_counter() - time_start_10_sec < time_to_show:
            time_old = perf_counter()
            # show 2 logo
            hori = np.concatenate((image1, image2), axis=1)

            cv2.namedWindow("programs", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("programs", 1680, 1000)
            cv2.imshow("programs", hori)
            if cv2.waitKey(1) == 27:
                break

            # We get a new frame from the webcam
            _, frame = webcam.read()
            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)
            frame = gaze.annotated_frame()

            pos = gaze.horizontal_ratio()
            # print(pos)

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

    print(logos_time)
    # удалить логотипы с наименьшем временем
    win_logos = []
    for item in logos_pair:
        if item[0] > item[1]:
            win_logos.append(filenames[item[1]])
        else:
            win_logos.append(filenames[item[0]])

    # print(win_logos)
    filenames = win_logos
    print(filenames)
    logos_time = [0] * len(filenames)
    logos_already_shows = []
    logos_pair = []

image = cv2.imread(f'{dir_path}/{filenames[0]}')
cv2.namedWindow("programs", cv2.WINDOW_NORMAL)
cv2.resizeWindow("programs", 1680, 1000)
cv2.imshow("programs", image)
while True:
    if cv2.waitKey(1) == 27:
        break


webcam.release()
cv2.destroyAllWindows()
