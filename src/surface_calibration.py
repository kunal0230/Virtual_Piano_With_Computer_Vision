import cv2
import numpy as np
import json

# Webcam settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

CALIBRATION_FRAMES = 100
calibration_count = 0
edge_positions = []  # Store detected edge y-coordinates

print("Desk Edge Calibration: Ensure the frame contains only the desk edge (no hands or fingers).")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the video feed
    frame = cv2.flip(frame, 1)

    # Convert to grayscale and apply edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Use Hough Line Transform to detect horizontal lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 5:  # Horizontal line
                edge_positions.append((y1 + y2) // 2)  # Average y-position
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    calibration_count += 1
    if calibration_count >= CALIBRATION_FRAMES:
        break

    # Show the video feed with detected edges
    cv2.putText(frame, "Calibrating Desk Edge...", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Desk Edge Calibration", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Calculate the final edge position as the median of collected values
if edge_positions:
    edge_y = int(np.median(edge_positions))
    print(f"Desk edge detected at y-coordinate: {edge_y}")

    # Save the edge position to a file
    with open("desk_edge_calibration.json", "w") as f:
        json.dump({"edge_y": edge_y}, f)
    print("Desk edge calibration saved to 'desk_edge_calibration.json'.")
else:
    print("Desk edge detection failed. Please try again.")
