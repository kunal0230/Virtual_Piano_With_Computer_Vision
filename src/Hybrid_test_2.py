import cv2
import mediapipe as mp
import numpy as np
from play_notes import SoundPlayer

# Notes assigned to fingertips for left and right hands
LEFT_HAND_NOTES = ['C4', 'D4', 'E4', 'F4', 'G4']
RIGHT_HAND_NOTES = ['A4', 'B4', 'C5', 'D5', 'E5']

# Webcam settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Mediapipe hand tracking with support for two hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.9)

# Sound player
player = SoundPlayer(LEFT_HAND_NOTES + RIGHT_HAND_NOTES)

# Tracking state
finger_pressed_left = [False] * 5  # Track pressed state for left hand fingers
finger_pressed_right = [False] * 5  # Track pressed state for right hand fingers
previous_positions_left = [None] * 5  # Previous fingertip positions for left hand
previous_positions_right = [None] * 5  # Previous fingertip positions for right hand
desk_edge_y = None  # Desk edge position

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
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Determine which hand is being tracked
            hand_label = results.multi_handedness[hand_idx].classification[0].label
            hand_type = "LEFT" if hand_label == "Left" else "RIGHT"
            hand_notes = LEFT_HAND_NOTES if hand_type == "LEFT" else RIGHT_HAND_NOTES
            finger_pressed = finger_pressed_left if hand_type == "LEFT" else finger_pressed_right
            previous_positions = previous_positions_left if hand_type == "LEFT" else previous_positions_right

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
            for idx, landmark_idx in enumerate(fingertip_indices):
                landmark = hand_landmarks.landmark[landmark_idx]
                fingertips.append((int(landmark.x * w), int(landmark.y * h)))

            # Smooth and calculate velocity
            for i, pos in enumerate(fingertips):
                smoothed_pos = smooth_position(pos, previous_positions[i])
                velocity = calculate_velocity(smoothed_pos, previous_positions[i])
                previous_positions[i] = smoothed_pos

                # Velocity-based press detection
                if velocity > 5 and not finger_pressed[i]:  # Key press
                    finger_pressed[i] = True
                    player.play_note_by_index(LEFT_HAND_NOTES.index(hand_notes[i]) if hand_type == "LEFT" else 5 + RIGHT_HAND_NOTES.index(hand_notes[i]))
                elif velocity < -3:  # Key release
                    finger_pressed[i] = False

                # Draw fingertips and note names
                color = (0, 255, 0) if finger_pressed[i] else (0, 0, 255)
                cv2.circle(frame, (int(smoothed_pos[0]), int(smoothed_pos[1])), 10, color, -1)
                cv2.putText(frame, hand_notes[i], (int(smoothed_pos[0]) + 10, int(smoothed_pos[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw desk edge
    cv2.line(frame, (0, desk_edge_y), (frame.shape[1], desk_edge_y), (255, 255, 0), 2)

    # Display the video feed
    cv2.putText(frame, "Advanced Virtual Piano", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Virtual Piano", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
