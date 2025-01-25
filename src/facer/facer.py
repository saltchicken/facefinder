from collections import Counter
from loguru import logger
from .analyze import get_embedding, get_embeddings_from_folder, get_embeddings_from_video
from .database import PostgresEmbeddingDatabase
from .utils.helper import classify_path

class Facer:
    def __init__(self):
        self.db = PostgresEmbeddingDatabase()

    def insert(self, name, input_file):
        match classify_path(input_file):
            case "folder":
                embeddings = get_embeddings_from_folder(input_file)
                for embedding in embeddings:
                    self.db.insert_embedding(name, embedding)
            case "image":
                try:
                    embedding = get_embedding(input_file)
                    self.db.insert_embedding(name, embedding)
                except Exception as e:
                    print(f"Failed to insert image: {e}")
            case "video":
                print("Not implemented for video")
            case _:
                print("Invalid input file")

    def match(self, input_file, threshold=0.85):
        match classify_path(input_file):
            case "folder":
                print("Not implemented for folders")
            case "image":
                try:
                    embedding = get_embedding(input_file)
                    result = self.db.match_embedding(embedding)
                    print(f"Result: {result}")
                except Exception as e:
                    print(f"Embedding failed to get match. Error: {e}")
            case "video":
                embeddings = get_embeddings_from_video(input_file)
                matches = []
                for embedding in embeddings:
                    try:
                        matched_name = self.db.match_embedding(embedding, threshold)
                        if matched_name:
                            matches.append(matched_name)
                    except Exception as e:
                        logger.debug(f"Failed to match embedding. Error: {e}")
                # num_frames = len(embeddings)
                # processed_frames = len(matches)
                # logger.debug(f"Processed {processed_frames} out of {num_frames} images")
                # if processed_frames < num_frames // 2:
                #     logger.debug("Not enough processed_frames")
                #     return "Unknown"
                if len(matches) == 0:
                    print("Unknown")
                    return

                counter = Counter(matches)
                print(counter)
                most_common_name, count = counter.most_common(1)[0]
                if count > len(matches) // 2:
                    print(most_common_name)
                else:
                    print("Unknown")
            case _:
                print("Invalid input file")

