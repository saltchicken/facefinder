from deepface import DeepFace
import cv2
import os
from loguru import logger
import tempfile
from fripper.ffmpeg_cmd import grab_thumbnails

class EmbeddingError(Exception):
    pass

def detect_face(input_image):
    image = cv2.imread(input_image)

    try:
        analysises = DeepFace.analyze(image, detector_backend="dlib", actions=['age', 'gender', 'emotion', 'race'])
        logger.debug("Analysises: ")
        logger.debug(analysises)

        for analysis in analysises:
            face = analysis["region"]
            x, y, w, h = face["x"], face["y"], face["w"], face["h"]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image with detected face
        cv2.imshow("Detected Face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        logger.debug(f"Error: {e}")

def get_embedding(input_image):
    image = cv2.imread(input_image)
    if image is None:
        raise EmbeddingError(f"Failed to read the input image: {input_image}")

    try:
        embedding_objs = DeepFace.represent(image, detector_backend="dlib", align=True)
        num_embeddings = len(embedding_objs)
        logger.debug(f"Found {len(embedding_objs)} faces")
        for embedding in embedding_objs:
            logger.debug(f"Facial Area: {embedding['facial_area']}")
            logger.debug(f"Face Confidence: {embedding['face_confidence']}")
            # logger.debug(f"Embedding Length: {len(embedding['embedding'])}")
            # logger.debug(f"Embedding: {embedding['embedding']}")
        if num_embeddings == 1:
            return embedding_objs[0]['embedding']
        elif num_embeddings > 1:
            raise EmbeddingError(f"Multiple embeddings found in image: {input_image} - TODO: Handle this")
        else:
            raise EmbeddingError(f"No Embeddings found in image: {input_image}")

    except Exception as e:
        raise EmbeddingError(f"An error occurred while processing the image: {e}")


def get_embeddings_from_folder(folder_path):
    # TODO: Make sure files are only images
    # folder_name = os.path.basename(os.path.normpath(folder_path))
    # logger.debug(f"Running on {folder_name}")
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    embeddings = []
    for file in files:
        logger.debug(file)
        embeddings.append(get_embedding(os.path.join(folder_path, file)))
    # return name, embeddings
    return embeddings

def get_embeddings_from_video(input_file):
    results = []
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = grab_thumbnails(input_file, temp_dir)
        for image_path in image_paths:
            try:
                embedding = get_embedding(image_path)
                results.append(embedding)
            except Exception as e:
                logger.debug(f"Failed to get embedding. Error: {e}")
        return results
