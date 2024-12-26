# main.py
import cv2
from screen_segmentation import segment_screen
from hand_tracking import get_fingertip_position
from interaction_detection import get_touched_section
from play_notes import play_note

# Configuration
NUM_SECTIONS = 8
NOTES = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Segment the screen
    frame = segment_screen(frame, NUM_SECTIONS)

    # Detect fingertip position
    fingertip_pos = get_fingertip_position(frame)

    # Detect which section is touched
    if fingertip_pos:
        section = get_touched_section(fingertip_pos, NUM_SECTIONS, frame.shape[1])
        if section is not None:
            play_note(NOTES[section])

    # Show the video feed
    cv2.imshow("Virtual Piano", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
