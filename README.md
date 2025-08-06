# Bad Apple played in Finder using Folders

Exactly what the title says.

# DEMO

[Youtube](https://www.youtube.com/watch?v=52e0vLNeWhM)

# Installation

1. Clone this repo
2. Find a way to download the Bad Apple!! original video
3. Reduce the frames of the video to <12 fps
4. Put the file into the same directory of ```frame-extracter```
5. Install the python dependencies: ```numpy^2.2.6``` and ```opencv-python^4.12.0.88```
6. In the directory "frame-extractor" run: ```python3 frame-extractor.py``` (it'll look for a video called ```bad-apple.mp4```)
7. Wait for the frames to be extracted
8. Go back a directory and run ```python3 player.py```

# Why did I make this?

Because funny Bad Apple!! meme on impressive things. I also wanted to stress-test how good the MacOS's Finder was, because I previously saw a video on a File Explorer (windows) version, which worked pretty well.

# Making of Frame Extractor

Because the resolution of the original video is 480:360, I decided on the perfect resolution for this project: 40:30 folders for a total of 1200 folders. The frame extractor analyses "chunks" of 1 frame from the video. Each of these chunks is 12x12 pixels big. For each of these chunks, the count-candidate algorithm is used to determine what color pixel is most present in the chunk. (Count-canidate was used to save RAM, especially because we're about to load 2629 frames into RAM... whooops). These chunks are iterated through until the whole frame is filled. This is then pushed to an array that holds all the frame information. After 1m 30s of frame extraction, it'll load all of the frame information into a JSON file. And we're done!

# Making of the Player

Making the player was pretty simple! All it needed to do was read the JSON file and create/delete folders based off of the frame information. My original idea was to fill in the entire area with folders, then if it was a white pixel, delete the folders where white pixels were present. Although this worked, it was pretty slow (even slower than it already is). I decided to optimize by NOT filling in the entire area with folders. Thus, the code only adds a folder if it's a black pixel, and only removes if its a white pixel. This drastically improved the speed. The only problem was speed, though, was Finder not refreshing fast enough. And because Apple decided to not add a refresh in Finder (???). I just decided to wait 0.5 seconds between each frame to allow Finder to refresh (still not slow enough).

# What did I learn?

I learned Finder is slow, and Apple should implement a manual refresh so I can make these stupid stuff.