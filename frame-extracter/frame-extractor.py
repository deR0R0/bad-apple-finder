import os
import sys
import cv2
import time
import json

def get_application_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return application_path
    return os.path.dirname(os.path.abspath(__file__))

# inputs
user_video_path = input("Enter the RELATIVE path to the video file (default is 'bad-apple.mp4'): ") or 'bad-apple.mp4'
user_video_path = os.path.join(get_application_path(), user_video_path)

if not os.path.exists(user_video_path):
    print(f"Video file '{user_video_path}' does not exist. Please check the path and try again.")
    exit(1)

vid = cv2.VideoCapture(user_video_path)

# getting pixel data
# we're going to get all the pixels within the range of 0-11 x
# then we're gonna see what color pixel is most present in the range via
# the count and candidate algorithm.
# we're gonna do this 40 times.
def get_area_pixels(image, y):
    area_pixels = []

    for x in range(40):
        count = 0
        candidate = [0, 0, 0]  # default candidate is black
        for x_range in range(12):
            for y_range in range(12):
                pixel_color = image[(y * 12) + y_range, (x * 12) + x_range]

                if pixel_color[0] > 151 and pixel_color[1] > 151 and pixel_color[2] > 151:  # white pixel/gray pixel
                    count += 1
                else:
                    count -= 1 # most likely black pixel

                # if the count is positive, we consider white to be the candidate
                if count > 0:
                    candidate = [253, 253, 253] # white pixel
                else:
                    candidate = [0, 0, 0] # black pixel

        area_pixels.append(candidate)

    return area_pixels

def get_frame_pixels(image):
    frame_pixels = []

    for y in range(30):
        area_pixels = get_area_pixels(image, y)
        frame_pixels.append(area_pixels)

    return frame_pixels


def get_all_frames():
    all_frames = []
    curr_frame = 1

    while True:
        success, frame = vid.read()
        if not success:
            break

        all_frames.append(get_frame_pixels(frame))
        print(f"Extracted frame {curr_frame}")
        curr_frame += 1

    pixels = {
        "pixels": all_frames
    }

    with open(os.path.join(get_application_path(), "frame_pixels.json"), "w") as f:
        json.dump(pixels, f)

# get all ze frames
start_time = time.time()
get_all_frames()
end_time = time.time()
print(f"Time taken to extract frames: {end_time - start_time} seconds")