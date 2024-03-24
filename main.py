import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

if __name__ == '__main__':
  
# For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
                continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks is not None:
                landmarks = results.pose_landmarks.landmark
                font = cv2.FONT_HERSHEY_COMPLEX
                if landmarks:

                    # Pushup detection done
                    if ((landmarks[11].visibility < 0.01) or (landmarks[30].visibility < 0.01)) == False:
                        push_compare1 = (landmarks[30].y / landmarks[12].y)
                        push_compare2 = (landmarks[29].y / landmarks[11].y)
                        if ((push_compare1 / push_compare2) >= 0.99) & ((push_compare1 / push_compare2) <= 1.01):
                            cv2.putText(image, "Push-up", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)

                    # if landmarks[11].y == landmarks[30].y and landmarks[12].y == landmarks[29].y:
                    #     cv2.putText(image, "HELLO WORLD", (400, 600), font, 3, (0, 255, 0), 12, cv2.LINE_AA)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()