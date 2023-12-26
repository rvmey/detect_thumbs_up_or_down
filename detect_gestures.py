import cv2
import requests, os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

debounce_timeout = 5        # Don't trigger the command any more than once per 5 seconds. 
confidence_threshold = .7   # Be 70 percent confident you see the gesture.

def debounce(timeout=5):
    def decorator(func):
        last_call = 0

        def wrapper(*args, **kwargs):
            nonlocal last_call
            current_time = time.time()

            if current_time - last_call >= timeout:
                last_call = current_time
                return func(*args, **kwargs)
            else:
                print(f"Function {func.__name__} is debounced and won't run.")
        return wrapper
    return decorator


# You have options for how to set triggercmd_token.  Keep it secret.
# triggercmd_token = os.getenv('TRIGGERCMD_TOKEN')
# triggercmd_token = <This is your token from the Instructions page. >

file_name = 'token.tkn'
file_path = os.path.expanduser(os.path.join('~', ".TRIGGERcmdData", file_name))
with open(file_path, 'r') as file:
    triggercmd_token = file.read()

@debounce(timeout=debounce_timeout)
def trigger_cmd(gesture):
    print("Running command with parameter: " + gesture)
    # This will trigger a command on one of your computers via TRIGGERcmd.
    # The command will run with thumb direction the last parameter.
    url = "https://www.triggercmd.com/api/run/trigger"
    json = {
        "computer": "laptop",
        "trigger": "notepad",
        "params": gesture
    }

    # For authorization
    headers = {
        "Authorization": "Bearer " + triggercmd_token
    }

    r = requests.post(url, headers=headers, json=json)

def main():
    # cap = cv2.VideoCapture("rtsp://admin:password@192.168.1.2:554/cam/realmonitor?channel=1&subtype=0")
    cap = cv2.VideoCapture(0)
    previous_gesture = "None"

    # Create an GestureRecognizer object.
    base_options = python.BaseOptions(model_asset_path='./gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        gesture = "None"
        recognition_result = recognizer.recognize(mp_image)
        if(len(recognition_result.gestures) > 0):
            top_gesture = recognition_result.gestures[0][0]
            if(top_gesture.score > confidence_threshold):
                gesture = str(top_gesture.category_name)

        if (gesture != "None"):
            cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Gesture Recognition', frame)

        # compare previous gesture to current
        if (previous_gesture == gesture):
            pass
        else:
            print(gesture)
            previous_gesture = gesture

            if previous_gesture == "None":
                pass
            else:
                trigger_cmd(gesture)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
