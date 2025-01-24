from deepface import DeepFace
import cv2
import os

def detect_face(input_image):
    image = cv2.imread(input_image)

    try:
        analysises = DeepFace.analyze(image, detector_backend="dlib", actions=['age', 'gender', 'emotion', 'race'])
        print("Analysises: ")
        print(analysises)

        for analysis in analysises:
            face = analysis["region"]
            x, y, w, h = face["x"], face["y"], face["w"], face["h"]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image with detected face
        cv2.imshow("Detected Face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")

def get_embedding(input_image):
    # TODO: Better error checking when file does not exist
    image = cv2.imread(input_image)

    try:
        embedding_objs = DeepFace.represent(image, detector_backend="dlib", align=True)
        num_embeddings = len(embedding_objs)
        print(f"Found {len(embedding_objs)} faces")
        for embedding in embedding_objs:
            print(f"Facial Area: {embedding['facial_area']}")
            print(f"Face Confidence: {embedding['face_confidence']}")
            # print(f"Embedding Length: {len(embedding['embedding'])}")
            # print(f"Embedding: {embedding['embedding']}")
        if num_embeddings == 1:
            return embedding_objs[0]['embedding']
        elif num_embeddings > 1:
            # TODO: Implement this or throw an error
            print("More than one embedding retrieved. This hasn't been handled yet")
            return None
        else:
            # TODO Throw an error here
            print("No embeddings found")
            return None

    except Exception as e:
        #TODO: This should throw an error
        print(f"Error: {e}")


def get_embeddings_from_folder(folder_path):
    # TODO: Make sure files are only images
    # folder_name = os.path.basename(os.path.normpath(folder_path))
    # print(f"Running on {folder_name}")
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    embeddings = []
    for file in files:
        print(file)
        embeddings.append(get_embedding(os.path.join(folder_path, file)))
    # return name, embeddings
    return embeddings



