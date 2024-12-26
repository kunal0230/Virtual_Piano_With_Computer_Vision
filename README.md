
# Virtual Piano with Computer Vision 🎹

This project is a **Virtual Piano** application built using **Computer Vision** and **Python**. The application leverages **Mediapipe** for hand tracking and **OpenCV** for desk edge detection. Users can play the piano by moving their fingers above a desk and tapping specific areas, which correspond to different musical notes.

---

## Features

- **Hand Tracking**: Detects fingers using Mediapipe and maps their movement to musical notes.
- **Velocity-Based Press**: Notes are triggered based on the velocity of finger movements.
- **Desk Edge Detection**: Dynamically detects the desk/table edge for accurate key presses.
- **Multi-Hand Support**: Tracks both left and right hands simultaneously.
- **Dynamic Calibration**: Supports dynamic desk edge and finger movement calibration for better accuracy.
- **Real-Time Visualizations**:
  - Displays note names on fingertips.
  - Shows currently pressed notes in a sidebar.

---

## Setup and Installation

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or above
- OpenCV
- Mediapipe
- Pygame

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kunal0230/Virtual_Piano_With_Computer_Vision.git
   cd Virtual_Piano_With_Computer_Vision
2. Install the required Python libraries:
  
        pip install -r requirements.txt

3. Run the calibration script to detect the desk edge:

       python src/surface_calibration.py

4. Play the Virtual Piano using the most optimized script:

        python src/Hybrid_test_2.py




### How the Virtual Piano Works

The Virtual Piano uses **computer vision** and **hand tracking** to simulate a real piano. Here's an explanation of how the system works step-by-step:

---

### 1. **Capturing the Video Input**
- The program uses the **webcam** to capture real-time video of the user's hands.
- The video feed is flipped horizontally to mimic a mirror, making the interaction more intuitive.

---

### 2. **Detecting the Desk Edge**
- **Purpose**: The desk edge is the virtual boundary representing the "keyboard" of the piano.
- The system analyzes the video feed to detect a straight horizontal line (desk edge) using edge detection techniques (e.g., Hough Line Transform).
- Once the desk edge is detected:
  - It serves as a reference point for finger movements.
  - The system uses this edge to determine when a finger "presses" a virtual key.

---

### 3. **Hand Tracking**
- The system uses **Mediapipe** to detect and track both hands.
- It identifies key points on the hands, such as the fingertips of the thumb, index, middle, ring, and pinky fingers.
- Each finger's movement is tracked independently.

---

### 4. **Mapping Fingers to Notes**
- Each fingertip is associated with a musical note:
  - **Left Hand**: C4, D4, E4, F4, G4
  - **Right Hand**: A4, B4, C5, D5, E5
- When a finger presses down near the desk edge, the corresponding note is played.

---

### 5. **Press Detection**
- The system detects a "key press" based on the **velocity** of finger movement:
  1. **Tracking Motion**: It tracks the position of each fingertip across consecutive frames.
  2. **Calculating Velocity**: It calculates the downward speed (velocity) of each fingertip.
  3. **Threshold-Based Trigger**:
     - If a fingertip moves downward quickly enough (velocity > threshold), it is interpreted as a key press.
     - If the finger moves back up, the system resets the press state, allowing the note to be played again.

---

### 6. **Playing the Notes**
- Once a "key press" is detected:
  - The corresponding note is played using the **Pygame mixer**.
  - Each note is associated with a sound file (e.g., `C4.mp3`, `D4.mp3`).
- Notes are only triggered once per downward motion to avoid repeated playback while the finger is stationary.

---

### 7. **Visual Feedback**
- The system provides real-time visualizations to enhance user interaction:
  - **Desk Edge**: A yellow horizontal line is drawn on the video feed, showing the detected desk edge.
  - **Fingertip Positions**: Fingertips are highlighted as circles:
    - **Green**: Indicates the finger is pressing a key.
    - **Red**: Indicates the finger is not pressing a key.
  - **Note Names**: The name of the note (e.g., C4, D4) is displayed near each fingertip.

---

### 8. **Multi-Hand Support**
- The system tracks both hands simultaneously, allowing users to:
  - Play multiple notes at once.
  - Use each hand independently for different sets of notes (left and right hand mapping).

---

### 9. **Dynamic Calibration**
- At startup, the system calibrates itself by:
  - Detecting the desk edge dynamically.
  - Identifying the range of motion for each fingertip.
- This ensures the system adapts to different setups, such as varying desk heights or camera angles.

---

### 10. **Real-Time Processing**
- The system processes video frames in real-time to ensure responsiveness.
- For every frame:
  1. Detect hands and desk edge.
  2. Track finger positions.
  3. Calculate velocities and detect key presses.
  4. Play notes and provide visual feedback.

---

### How the User Interacts with the Virtual Piano

1. **Setup**:
   - Place the webcam so that your hands and the desk edge are visible.
   - Run the script and wait for the desk edge calibration to complete.
2. **Playing Notes**:
   - Move your hands above the desk.
   - Tap your fingers downward toward the desk edge to play notes.
   - The system will detect which finger is moving and play the corresponding note.
3. **Feedback**:
   - Watch the screen to see visual indicators:
     - Fingertip positions.
     - Desk edge.
     - Names of the notes being played.

---

### Key Features of the Virtual Piano

1. **Desk Edge as a Virtual Keyboard**:
   - Acts as a boundary for detecting key presses.
   - Allows for precise interaction between the user's fingers and the virtual piano.
2. **Velocity-Based Key Press**:
   - Notes are triggered based on the speed of downward motion, mimicking the tactile feel of pressing a real piano key.
3. **Multi-Hand and Multi-Finger Support**:
   - Tracks both hands and all 10 fingers simultaneously.
   - Enables complex playing, including chords.
4. **Dynamic Adaptability**:
   - Adapts to different physical setups by dynamically detecting the desk edge and calibrating finger movements.
5. **Real-Time Feedback**:
   - Provides visual cues for easier interaction and learning.

---

### Advantages of the System

1. **Accessibility**:
   - Works with any standard webcam and desk setup.
   - No physical piano is required.
2. **Adaptability**:
   - Automatically adjusts to different environments and desk configurations.
3. **Engagement**:
   - Real-time visual feedback makes it easy to use and engaging for beginners.
4. **Scalability**:
   - Can be extended to include more advanced features like chords, custom note mappings, or gesture-based controls.

---

### Future Enhancements

1. **Chord Detection**:
   - Enable the system to detect and play multiple notes simultaneously.
2. **Custom Note Mapping**:
   - Allow users to configure their own note mappings for each finger.
3. **Augmented Reality Integration**:
   - Add virtual piano keys on the desk for a more immersive experience.
4. **Gesture-Based Features**:
   - Introduce swipes or other gestures for additional functionalities (e.g., changing octaves).
















### File Structure

#### Main Files
- **`src/Hybrid_test_2.py`**: The best working version of the Virtual Piano application.
- **`src/main.py`**: Initial prototype with basic functionality.
- **`src/Hybrid_test.py`**: Another iteration with refined logic.

#### Resources
- **`resources/sounds/`**: Contains `.mp3` files for different musical notes (e.g., C4, D4, E4, etc.).

#### Supporting Files
- **`src/hand_tracking.py`**: Handles hand and fingertip tracking using Mediapipe.
- **`src/interaction_detection.py`**: Detects interactions like finger touches.
- **`src/screen_segmentation.py`**: Divides the screen into sections for better visualization.
- **`src/play_notes.py`**: Plays notes using Pygame when fingers touch specific areas.
- **`src/surface_calibration.py`**: Calibrates the desk/table surface for accurate detection.

---

### How to Use

1. Place your hands above the desk and ensure the desk edge is visible on the camera.
2. Use the script (`Hybrid_test_2.py`) to track your hands and play notes.
3. Move your fingers downward quickly to "press" a key, triggering a sound.
4. View the real-time visualizations:
   - Fingertip positions and note names.
   - Notes currently being played on the sidebar.

---

### Future Improvements

- **Chord Support**: Enable simultaneous notes for more realistic piano playing.
- **Customizable Notes**: Allow users to assign custom notes to fingers.
- **Advanced Gestures**: Incorporate gestures like hand swipes for additional functionalities.
- **AR Guidelines**: Add augmented reality visualizations for virtual piano keys on the desk.

        
