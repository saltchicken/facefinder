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


    def average_embedding(self, name, embedding):
        import ast
        with self.conn.cursor() as cursor:
            # Start a transaction explicitly
            cursor.execute("BEGIN;")

            # Get the current data from the table
            cursor.execute(
                """
                SELECT embedding, embedding_count
                FROM embeddings
                WHERE name = %s;
                """, 
                (name,)
            )
            current_data = cursor.fetchone()

            if current_data:
                average_embedding, embedding_count = current_data

                # TODO: This is a terrible hack. Clean up type guessing
                # Ensure both `average_embedding` and `embedding` are lists of floats
                try:
                    # Convert string to a list (if it's stored as a string)
                    if isinstance(average_embedding, str):
                        average_embedding = ast.literal_eval(average_embedding)

                    if not isinstance(average_embedding, list):
                        raise ValueError("average_embedding must be a list.")

                    # Ensure embedding is a list of floats
                    if not isinstance(embedding, list):
                        embedding = [float(emb) for emb in embedding]

                    # Calculate the new average and embedding count
                    new_average_embedding = [
                        (embedding_count * avg + emb) / (embedding_count + 1)
                        for avg, emb in zip(average_embedding, embedding)
                    ]
                    new_embedding_count = embedding_count + 1
                    # Update the table with the new values
                    cursor.execute(
                        """
                        UPDATE embeddings
                        SET embedding = %s,
                            embedding_count = %s
                        WHERE name = %s;
                        """,
                        (new_average_embedding, new_embedding_count, name)
                    )
                except Exception as e:
                    print(f"Error: {e}")
            
            # Commit the transaction
            self.conn.commit()

    def delete_record(name):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM embeddings
                WHERE name = %s
                """,
                (name,)
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
                (name,)
            ).fetchall()

        if len(result) > 0:
            return True
        else:
            return False
