import cv2
import json
from hand_tracking import HandTracker
from play_notes import SoundPlayer

# Notes assigned to fingertips
LEFT_HAND_NOTES = ['C4', 'D4', 'E4', 'F4', 'G4']
RIGHT_HAND_NOTES = ['A4', 'B4', 'C5', 'D5', 'E5']
NOTES = LEFT_HAND_NOTES + RIGHT_HAND_NOTES

# Load pre-calibrated desk edge position
try:
    with open("desk_edge_calibration.json", "r") as f:
        edge_data = json.load(f)
        edge_y = edge_data["edge_y"]
        print(f"Loaded desk edge position: {edge_y}")
except FileNotFoundError:
    print("Desk edge calibration file not found. Please run 'desk_edge_calibration.py' first.")
    exit(1)

# Webcam settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Hand tracker and sound player
hand_tracker = HandTracker(max_hands=2, model_complexity=1)
player = SoundPlayer(NOTES)

# Press detection settings
PRESS_THRESHOLD = 5  # Proximity to the desk edge to trigger a press
finger_pressed = {i: False for i in range(10)}  # Track if a finger has pressed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the video feed
    frame = cv2.flip(frame, 1)

    # Hand tracking
    hands_data = hand_tracker.get_all_fingertips(frame)
    if hands_data:
        hands_data.sort(key=lambda h: 0 if h['hand'] == 'left' else 1)

    # Extract fingertip positions
    fingertips_ordered = []
    for hand_info in hands_data:
        fingertips_2d = [p[:2] for p in hand_info['fingertips_3d']]
        fingertips_ordered.extend(fingertips_2d)

    # Ensure exactly 10 fingers
    while len(fingertips_ordered) < 10:
        fingertips_ordered.append(None)
    fingertips_ordered = fingertips_ordered[:10]

    # Press detection
    for i, pos in enumerate(fingertips_ordered):
        if pos is None:
            finger_pressed[i] = False
            continue

        # Check if the finger is near the desk edge
        distance_to_edge = abs(pos[1] - edge_y)
        if distance_to_edge <= PRESS_THRESHOLD and not finger_pressed[i]:
            finger_pressed[i] = True
            player.play_note_by_index(i)
        elif distance_to_edge > PRESS_THRESHOLD:
            # Reset the press state when the finger moves away
            finger_pressed[i] = False

    # Visualization
    for i, pos in enumerate(fingertips_ordered):
        if pos is not None:
            color = (0, 255, 0) if finger_pressed[i] else (0, 0, 255)
            cv2.circle(frame, (int(pos[0]), int(pos[1])), 10, color, -1)
            cv2.line(frame, (0, edge_y), (frame.shape[1], edge_y), (255, 255, 0), 2)

    # Display the video feed
    cv2.putText(frame, "Desk Edge Virtual Piano", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Virtual Piano", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
