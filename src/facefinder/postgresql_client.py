import psycopg
from dotenv import load_dotenv
import numpy as np
import os
# from pgvector.psycopg import register_vector

load_dotenv()

class EmbeddingDatabase:
    def __init__(self):
        # Establish a persistent connection when the object is initialized
        self.connection_string = f"postgres://{os.getenv('USER')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
        print(self.connection_string)
        self.conn = psycopg.connect(self.connection_string)

    def __enter__(self):
        # Allows usage in a context manager
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing connection to database")
        if self.conn:
            self.conn.close()

    def insert_embedding(self, name, embedding):
        embedding = np.array(embedding)

        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO embeddings (name, embedding) VALUES (%s, %s)",
                (name, embedding.tolist())
            )
            self.conn.commit()

    def check_embedding(self, embedding):
        embedding = np.array(embedding)

        with self.conn.cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name, (embedding <-> %s::vector) AS euclidean_distance
                FROM embeddings
                ORDER BY euclidean_distance
                LIMIT 5
                """,
                (embedding.tolist(),)
            ).fetchall()

        return result

