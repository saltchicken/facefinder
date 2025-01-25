from fripper.ffmpeg_cmd import grab_thumbnails
import tempfile
from .analyze import get_embedding, get_embeddings_from_folder, match_list_of_embeddings
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
                # with tempfile.TemporaryDirectory() as temp_dir:
                #     temp_dir_path = Path(temp_dir)
                #     output_file = temp_dir_path / "image.jpg"
                #     grab_thumbnails(input_file, output_file)
            case _:
                print("Invalid input file")

    def match(self, input_file, threshold=0.85):
        match classify_path(input_file):
            case "folder":
                print("Not implemented for folders")
            case "image":
                try:
                    embedding = get_embedding(input_file)
                    result = self.db.check_embedding(embedding)
                    print(f"Result: {result}")
                except Exception as e:
                    print(f"Embedding failed to get match. Error: {e}")
            case "video":
                with tempfile.TemporaryDirectory() as temp_dir:
                    image_paths = grab_thumbnails(input_file, temp_dir)
                    result = match_list_of_embeddings(image_paths, self.db)
                    print(result)
            case _:
                print("Invalid input file")

