import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

class EmbeddingDatabase:
    def __init__(self):
        # Establish a persistent connection when the object is initialized
        self.connection_string = f"postgres://{os.getenv('USER')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
        # print(self.connection_string)
        self.conn = psycopg.connect(self.connection_string)

    def close(self):
        print("Closing connection to database")
        if self.conn:
            self.conn.close()

    def __enter__(self):
        # Allows usage in a context manager
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def insert_embedding(self, name, embedding):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO embeddings (name, embedding) VALUES (%s, %s)",
                (name, embedding) 
            )
            self.conn.commit()

    def check_embedding(self, embedding):
        with self.conn.cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name, (embedding <-> %s::vector) AS euclidean_distance
                FROM embeddings
                ORDER BY euclidean_distance
                LIMIT 5
                """,
                (embedding,)
            ).fetchall()

        return result

    def does_name_exist(self, name):
        with self.conn.cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name
                FROM embeddings
                WHERE name = %s
                """,
                (name)
            ).fetchall()

        return result
