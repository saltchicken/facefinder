import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Load image
image = cv2.imread('c:/users/saltchicken/desktop/test2.png')

# Convert the image to RGB (MediaPipe uses RGB, OpenCV uses BGR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process the image and get face landmarks
results = face_mesh.process(image_rgb)

if results.multi_face_landmarks:
    for landmarks in results.multi_face_landmarks:
        # Draw face mesh landmarks
        mp_drawing.draw_landmarks(image, landmarks, mp_face_mesh.FACEMESH_TESSELATION)

        # Access key landmarks for orientation detection (such as eyes, nose, mouth)
        nose_tip = landmarks.landmark[1]  # Nose tip landmark
        left_eye = landmarks.landmark[33]  # Left eye
        right_eye = landmarks.landmark[133]  # Right eye
        mouth_left = landmarks.landmark[61]  # Left corner of the mouth
        mouth_right = landmarks.landmark[291]  # Right corner of the mouth

        # Get vertical positions (y-coordinates) of important landmarks
        eye_y = (left_eye.y + right_eye.y) / 2  # Average y-coordinate of the eyes
        nose_y = nose_tip.y  # Y-coordinate of the nose tip
        mouth_y = (mouth_left.y + mouth_right.y) / 2  # Average y-coordinate of the mouth

        # Determine if the face is looking up, down, or straight based on vertical positions
        if eye_y < nose_y and mouth_y < nose_y:
            cv2.putText(image, "Looking Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif eye_y > nose_y and mouth_y > nose_y:
            cv2.putText(image, "Looking Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Looking Straight", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Show the output image
cv2.imshow('Face Orientation Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

