import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import mediapipe as mp
import av

st.title("Hand Finger Counter")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class HandDetector(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.flip(img, 1)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        finger_count = 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark
                tips = [4, 8, 12, 16, 20]
                fingers = []

                if landmarks[tips[0]].x < landmarks[tips[0]-1].x:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for tip in tips[1:]:
                    if landmarks[tip].y < landmarks[tip-2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_count = fingers.count(1)

                cv2.putText(
                    img,
                    str(finger_count),
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 255, 0),
                    5
                )

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


webrtc_streamer(
    key="hand-counter",
    video_processor_factory=HandDetector,
)
