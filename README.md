# Detect thumbs up or down with computer vision, and trigger a command on a remote computer via TRIGGERcmd with Up or Down as the parameter 

This script will trigger a command on one of your computers when your camera detects a thumbs up or down.  

The command will be triggered via TRIGGERcmd.com, and the parameter of the command will be Up or Down depending on which one you showed the camera. 

## Prereq's:

```
pip install opencv-python
pip install mediapipe
pip install requests
```

## Run it like this:

    python3 detect_thumb_up_or_down.py

## See it in action here:

[![Watch the video](https://img.youtube.com/vi/70RW8wRU7kg/default.jpg)](https://youtu.be/70RW8wRU7kg)

## Forum post:

https://www.triggercmd.com/forum/topic/2776/trigger-commands-with-vision-python-script

## New and improved version:

detect_gestures.py uses MediaPipe's hand gesture recognition to recognize 7 different gestures, and it prevents your command from running more than once every 5 seconds.  

- Closed Fist
- Open Palm
- Pointing Up
- Thumbs Down
- Thumbs Up
- Victory
- I Love You

See this for details:
https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python