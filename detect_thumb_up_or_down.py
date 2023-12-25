import cv2              # Prereq:  pip install opencv-python
import mediapipe as mp  # Prereq:  pip install mediapipe
import requests         # Prereq:  pip install requests
import os

# You have options for how to set triggercmd_token.  Keep it secret.
# triggercmd_token = os.getenv('TRIGGERCMD_TOKEN')
# triggercmd_token = <This is your token from the Instructions page. >

file_name = 'token.tkn'
file_path = os.path.expanduser(os.path.join('~', ".TRIGGERcmdData", file_name))
with open(file_path, 'r') as file:
    triggercmd_token = file.read()

def trigger_cmd(direction):
    print(direction)

    # This will trigger a command on one of your computers via TRIGGERcmd.
    # The command will run with thumb direction the last parameter.
    url = "https://www.triggercmd.com/api/run/trigger"
    json = {
        "computer": "laptop",
        "trigger": "notepad",
        "params": direction
    }

    # For authorization
    headers = {
        "Authorization": "Bearer " + triggercmd_token
    }

    r = requests.post(url, headers=headers, json=json)


def detect_thumbs_direction(frame):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmarks for the thumb and index finger
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Check the vertical position of the thumb compared to the index finger
            if thumb_tip.y < index_finger_tip.y:
                return "Up"
            else:
                return "Down"

    return "Not Detected"

def main():
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera
    previous_thumbs_direction_default = "Not Detected"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Detect thumbs direction
        thumbs_direction = detect_thumbs_direction(frame)

        # Compare previous thumbs direction to current
        if (previous_thumbs_direction_default == thumbs_direction):
            pass
        else:
            if previous_thumbs_direction_default == "Not Detected":
                trigger_cmd(thumbs_direction)

        # Display the result on the frame
        cv2.putText(frame, f"Thumbs Direction: {thumbs_direction}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Thumbs Direction Detection', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
