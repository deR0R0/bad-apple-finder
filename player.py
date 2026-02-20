import os
import subprocess
import json
import time
import sys

def get_application_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return application_path
    return os.path.dirname(os.path.abspath(__file__))

all_frames = json.load(open(os.path.join(get_application_path(), "frame_pixels.json"), "r"))
frame_pixels = all_frames["pixels"]
delay_time = 0.5
directoryName = "abc"

print("Successfully loaded " + str(len(frame_pixels)) + " frames.")
print("Ready to play Bad Apple!! Make sure Finder is the correct width and height")

def play_frame(frame_number):
    count = 0

    for row in frame_number:
        for pixel in row:
            count += 1
            
            # check for white pixel
            if pixel == [253, 253, 253]:
                # check if theres already a folder there
                if os.path.exists(os.path.join(get_application_path(), f"./{directoryName}/{count}/")):
                    # remove the folder if it exists
                    os.rmdir(os.path.join(get_application_path(), f"./{directoryName}/{count}/"))
            else: # black pixel? create a folder if it doesn't exist
                if not os.path.exists(os.path.join(get_application_path(), f"./{directoryName}/{count}/")):
                    os.makedirs(os.path.join(get_application_path(), f"./{directoryName}/{count}/"))

    script = '''
    tell application "Finder"
        if (count of Finder windows) > 0 then
            set theWin to front window
            set theTarget to target of theWin
            set target of theWin to theTarget
        end if
    end tell
    '''
    subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL) # refresh finder, use Popen to avoid waiting for it to finish

    

def play_all_frames():
    curr_frame = 0
    start_time = time.time()

    for frame in frame_pixels:
        play_frame(frame)
        curr_frame += 1
        print(f"Played frame {curr_frame}")
        time.sleep(delay_time) # add delay to allow finder to refresh

    print(f"Finished playing all frames in {time.time() - start_time:.2f} seconds.")

user_delay_time = input("Enter delay time between frames in seconds (default is 0.5): ")
if user_delay_time:
    try:
        delay_time = float(user_delay_time)
        print(f"Using delay time of {delay_time} seconds.")
        print(f"Estimated total play time: {delay_time * len(frame_pixels) / 60:.2f} minutes.")
    except ValueError:
        print("Invalid input, using default delay time of 0.5 seconds.")
        delay_time = 0.5

# make sure to fill in everything for the first
# frame of the video
play_frame(frame_pixels[0])

input("[ENTER] Start Playing Bad Apple!!")

play_all_frames()