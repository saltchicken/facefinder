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

        # Access key landmarks for orientation detection (such as nose, eyes, mouth)
        nose_tip = landmarks.landmark[1]  # Nose tip landmark
        left_eye = landmarks.landmark[33]  # Left eye
        right_eye = landmarks.landmark[133]  # Right eye
        left_ear = landmarks.landmark[234]  # Left ear
        right_ear = landmarks.landmark[454]  # Right ear

        # Check symmetry of the face by comparing positions of eyes, nose, and ears
        if abs(left_eye.x - right_eye.x) < 0.05 and abs(left_eye.y - right_eye.y) < 0.05:
            # If eyes are close to being aligned, it is likely a frontal face
            cv2.putText(image, "Frontal Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # If the eyes are not aligned, it is likely a profile
            cv2.putText(image, "Side Profile", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Show the output image
cv2.imshow('Face Orientation Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

