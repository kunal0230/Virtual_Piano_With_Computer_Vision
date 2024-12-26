import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self, max_hands=2, model_complexity=1):
        self.mp_hands_module = mp.solutions.hands
        self.mp_hands = self.mp_hands_module.Hands(
            model_complexity=model_complexity,
            max_num_hands=max_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_all_fingertips(self, frame):
        """
        Returns a list of dictionaries containing hand data:
        {
          'hand': 'left' or 'right',
          'fingertips_3d': [(x, y, z) for thumb, index, middle, ring, pinky]
        }
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(rgb_frame)

        hands_data = []
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label.lower()  # 'left' or 'right'
                h, w, _ = frame.shape

                # Extract fingertip positions
                fingertip_indices = [
                    self.mp_hands_module.HandLandmark.THUMB_TIP,
                    self.mp_hands_module.HandLandmark.INDEX_FINGER_TIP,
                    self.mp_hands_module.HandLandmark.MIDDLE_FINGER_TIP,
                    self.mp_hands_module.HandLandmark.RING_FINGER_TIP,
                    self.mp_hands_module.HandLandmark.PINKY_TIP,
                ]
                fingertips_3d = []
                for idx in fingertip_indices:
                    lm = hand_landmarks.landmark[idx]
                    fx, fy, fz = lm.x * w, lm.y * h, lm.z
                    fingertips_3d.append((fx, fy, fz))

                hands_data.append({
                    'hand': hand_label,
                    'fingertips_3d': fingertips_3d,
                })
        return hands_data
