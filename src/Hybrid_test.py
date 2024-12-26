import cv2
import mediapipe as mp
import numpy as np
from play_notes import SoundPlayer

# Notes assigned to fingertips
LEFT_HAND_NOTES = ['C4', 'D4', 'E4', 'F4', 'G4']
RIGHT_HAND_NOTES = ['A4', 'B4', 'C5', 'D5', 'E5']
NOTES = LEFT_HAND_NOTES + RIGHT_HAND_NOTES

# Webcam settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Mediapipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Sound player
player = SoundPlayer(NOTES)

# Press detection settings
PRESS_THRESHOLD = 10  # Proximity to the desk edge to trigger a press
velocity_threshold_down = 5  # Velocity threshold for key press
velocity_threshold_up = -3  # Velocity threshold for key release
finger_pressed = {i: False for i in range(10)}  # Track pressed state
previous_positions = [None] * 10  # Track previous fingertip positions
current_velocities = [0] * 10  # Track fingertip velocities
currently_pressed_notes = []  # Track currently pressed notes
desk_edge_y = None  # Initialize desk edge position

# Exponential smoothing function
def smooth_position(current, previous, alpha=0.3):
    if previous is None:
        return current
    return tuple(alpha * c + (1 - alpha) * p for c, p in zip(current, previous))

# Detect desk edge using Hough Line Transform
def detect_desk_edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 5:  # Horizontal line
                return (y1 + y2) // 2  # Return the y-coordinate of the desk edge
    return None

# Calculate velocity for a fingertip
def calculate_velocity(current, previous):
    if current is None or previous is None:
        return 0
    return current[1] - previous[1]  # Change in y-coordinate

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the video feed
    frame = cv2.flip(frame, 1)

    # Desk edge detection
    if desk_edge_y is None:
        desk_edge_y = detect_desk_edge(frame)
    if desk_edge_y is None:
        cv2.putText(frame, "Desk Edge Not Detected. Please ensure the desk is visible.", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Virtual Piano", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Hand tracking
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract fingertip positions
            h, w, _ = frame.shape
            fingertip_indices = [
                mp_hands.HandLandmark.THUMB_TIP,
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]
            fingertips = []
            for idx in fingertip_indices:
                landmark = hand_landmarks.landmark[idx]
                fingertips.append((int(landmark.x * w), int(landmark.y * h)))

            # Smooth fingertip positions and calculate velocity
            for i, pos in enumerate(fingertips):
                smoothed_pos = smooth_position(pos, previous_positions[i])
                velocity = calculate_velocity(smoothed_pos, previous_positions[i])
                previous_positions[i] = smoothed_pos
                current_velocities[i] = velocity

                # Velocity-based press detection
                note = NOTES[i]
                if velocity > velocity_threshold_down and not finger_pressed[i]:
                    finger_pressed[i] = True
                    currently_pressed_notes.append(note)
                    currently_pressed_notes = list(set(currently_pressed_notes))  # Avoid duplicates
                    player.play_note_by_index(i)
                elif velocity < velocity_threshold_up:
                    finger_pressed[i] = False
                    if note in currently_pressed_notes:
                        currently_pressed_notes.remove(note)

                # Draw fingertips and note names
                color = (0, 255, 0) if finger_pressed[i] else (0, 0, 255)
                cv2.circle(frame, (int(smoothed_pos[0]), int(smoothed_pos[1])), 10, color, -1)
                cv2.putText(frame, note, (int(smoothed_pos[0]) + 10, int(smoothed_pos[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw desk edge
    cv2.line(frame, (0, desk_edge_y), (frame.shape[1], desk_edge_y), (255, 255, 0), 2)

    # Draw sidebar with currently pressed notes
    sidebar_x = frame.shape[1] - 200
    cv2.rectangle(frame, (sidebar_x, 0), (frame.shape[1], frame.shape[0]), (50, 50, 50), -1)
    cv2.putText(frame, "Pressed Notes", (sidebar_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    for idx, note in enumerate(currently_pressed_notes):
        cv2.putText(frame, note, (sidebar_x + 10, 60 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the video feed
    cv2.putText(frame, "Refined Virtual Piano", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Virtual Piano", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
