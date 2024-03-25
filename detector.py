import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class detector:
    def __init__(self, cap, type):
        self.type = type
        self.image = None
        self.cap = cap

    def change_type(self, type):
        self.type = type
  
# For webcam input:
    def update(self):
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            success, self.image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
                return

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
            self.image.flags.writeable = False
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            results = pose.process(self.image)
            resultPose = ""
            if results.pose_landmarks is not None:
                landmarks = results.pose_landmarks.landmark
                font = cv2.FONT_HERSHEY_COMPLEX
                if landmarks:
                    if self.type == "Pushups":
                    # Pushup detection done
                            if landmarks[12].visibility > landmarks[11].visibility:
                                mark = [12, 30]
                            else:
                                mark = [11, 29]
                            comparison = (landmarks[mark[0]].y / landmarks[mark[1]].y)
                            if (comparison >= 0.99) & (comparison <= 1.01):
                                resultPose = "Pushups"
                                cv2.putText(self.image, "Push-up", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)
                                time.sleep(2)
                    if self.type == "Squats":
                        if ((landmarks[24].visibility < 0.1) or (landmarks[23].visibility < 0.1) or (landmarks[26].visibility < 0.1) or (landmarks[25].visibility < 0.1)) == False:
                            sit_compare1 = (landmarks[23].y / landmarks[25].y)
                            sit_compare2 = (landmarks[24].y / landmarks[26].y)
                            if ((sit_compare1/sit_compare2 >= 0.99)) & ((sit_compare1 / sit_compare2) <= 1.01):
                                resultPose = "Squats"
                                cv2.putText(self.image, "Sit-up", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)
                    
                    if self.type == "Situps":
                        cv2.putText(self.image, "Work in progress :)", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)




                    # if landmarks[11].y == landmarks[30].y and landmarks[12].y == landmarks[29].y:
                    #     cv2.putText(image, "HELLO WORLD", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)

            # Draw the pose annotation on the image.
            self.image.flags.writeable = True
            #self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                self.image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            self.image = cv2.flip(self.image, 1)
            return self.image, resultPose
            
