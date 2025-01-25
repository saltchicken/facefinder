from deepface import DeepFace
import cv2
import os
from collections import Counter
from loguru import logger

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

def match_list_of_embeddings(image_paths, db):
    # TODO: Return confidence as well
    results = []
    # for image_path in image_paths:
    #     try:
    #         embedding = get_embedding(image_path)
    #         results.append(db.check_embedding(embedding)[0])
    #     except Exception as e:
    #         logger.debug(f"Embedding failed to get match. Error: {e}")
    # logger.debug(f"Processed {len(results)} out of {len(image_paths)} images")
    # all_same = all(result[0] == results[0][0] for result in results)
    # if all_same:
    #     return results[0][0]
    # else:
    #     logger.debug("Frames did not return same match. Return `Unknown`")
    #     logger.debug(results)
    #     return "Unknown"
    tolerance = 0.85
    for image_path in image_paths:
        try:
            embedding = get_embedding(image_path)
            checked_embedding = db.check_embedding(embedding)[0]
            if checked_embedding[1] < tolerance:
                results.append(checked_embedding[0])
            else:
                logger.debug(f"Embedding failed confidence check of tolerance {tolerance}")
        except Exception as e:
            logger.debug(f"Embedding failed to get match. Error: {e}")
    num_frames = len(image_paths)
    processed_frames = len(results)
    logger.debug(f"Processed {processed_frames} out of {num_frames} images")
    if processed_frames < num_frames // 2:
        logger.debug("Not enough processed_frames")
        return "Unknown"
    counter = Counter(results)
    most_common_name, count = counter.most_common(1)[0]
    if count > len(results) // 2:
        return most_common_name
    else:
        return "Unknown"



