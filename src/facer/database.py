import psycopg
from psycopg.errors import OperationalError
import os
from env_loader import EnvLoader

from loguru import logger


class PostgresEmbeddingDatabase:
    def __init__(self):
        env_loader = EnvLoader("facer", [
                ("DB_HOST", "localhost"),
                ("DB_PORT", "5432"),
                ("DB_USER", "postgres"),
                ("DB_NAME", "postgres"),
                ("DB_PASSWORD", ""),
            ])
        self.connect()

    def connect(self):
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")

        if password:
            self.connection_string = (
                f"postgres://{user}:{password}@{host}:{port}/{database}"
                f"?connect_timeout=5"
            )
        else:
            self.connection_string = (
                f"postgres://{user}@{host}:{port}/{database}"
                f"?connect_timeout=5"
            )

        try:
            self.conn = psycopg.connect(self.connection_string)
            print(f"Connection established")
            self.connection_status = True
        except OperationalError as e:
            print(f"Failed to connect to database: {e}")
            print(
                "If you have not set a .env file, please set the following environment variables: USER, HOST, PORT, DB_NAME"
            )
            self.connection_status = False

        logger.debug(f"Check for existence of required tables")

        embeddings_table_exists = self.check_table_existence("embeddings", "public")
        averaged_embeddings_table_exists = self.check_table_existence("averaged_embeddings", "public")

        if embeddings_table_exists and averaged_embeddings_table_exists:
            logger.debug("Tables exist")
        else:
            logger.warning("Tables do not exist. Running table initialization.")
            self.initialize_tables()


    def close(self):
        print("Closing connection to database")
        if self.conn:
            self.conn.close()
            self.connection_status = False

    def __enter__(self):
        # Allows usage in a context manager
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def insert_embedding(self, name, embedding):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO embeddings (name, embedding)
                SELECT %s, %s
                WHERE NOT EXISTS ( SELECT 1 FROM embeddings WHERE embedding = %s::vector );
                """,
                (name, embedding, embedding),
            )
            self.conn.commit()

    def average_embeddings(self, name):
        with self.conn.cursor() as cursor:
            cursor.execute(
                    """
                    WITH avg_embedding AS (
                            SELECT name, AVG(embedding) AS average_embedding
                            FROM embeddings
                            WHERE name = %s
                            GROUP BY name
                        )
                        UPDATE averaged_embeddings
                        SET averaged_embedding = (SELECT average_embedding FROM avg_embedding)
                        WHERE name = (SELECT name FROM avg_embedding);
                    """,
                    (name,),
                )
            cursor.execute(
                """
                    WITH avg_embedding AS (
                        SELECT name, AVG(embedding) AS average_embedding
                        FROM embeddings
                        WHERE name = %s
                        GROUP BY name
                    )

                    -- Insert if no rows were updated
                    INSERT INTO averaged_embeddings (name, averaged_embedding)
                    SELECT name, average_embedding
                    FROM avg_embedding
                    WHERE NOT EXISTS (
                        SELECT 1 FROM averaged_embeddings WHERE name = (SELECT name FROM avg_embedding)
                    );
                """,
                (name,),
            )
            self.conn.commit()


    def delete_record(name):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM embeddings
                WHERE name = %s
                """,
                (name,),
            )
            self.conn.commit()

    def match_embedding(self, embedding, threshold=None):
        with self.conn.cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name, (averaged_embedding <-> %s::vector) AS euclidean_distance
                FROM averaged_embeddings
                ORDER BY euclidean_distance
                LIMIT 1
                """,
                (embedding,),
            ).fetchall()[0]

        if threshold:
            if result[1] <= threshold:
                logger.debug(f"Matched embedding with name: {result[0]} with distance: {result[1]}")
                return result[0]
            else:
                logger.debug(f"No embeddings matched that met the threshold of {threshold}")
                return None
        else:
            return result[0]

    def does_name_exist(self, name):
        with self.conn.cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name
                FROM embeddings
                WHERE name = %s
                """,
                (name,),
            ).fetchall()

        if len(result) > 0:
            return True
        else:
            return False

    def initialize_tables(self):
        try:
            with self.conn.cursor() as cursor:
                logger.info("Initializing vector extension.")
                cursor.execute(
                    """
                    CREATE EXTENSION IF NOT EXISTS vector;
                    """
                )
                logger.info("Creating 'embeddings' table.")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS embeddings (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        embedding VECTOR(4096) NOT NULL
                    )
                    """
                )
                logger.info("Creating 'averaged_embeddings' table.")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS averaged_embeddings (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    averaged_embedding VECTOR(4096) NOT NULL
                    )
                    """
                )
                self.conn.commit()
                logger.info("Tables initialized successfully.")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error initializing tables: {e}")
            raise
    
    def check_table_existence(self, table_name, schema='public'):
        try:
            with self.conn.cursor() as cursor:
                exists = cursor.execute(
                    """
                    SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = %s and table_name = %s
                    );
                    """,
                    (schema, table_name),
                ).fetchone()[0]

                if exists:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(f"Error checking table existence: {e}")
            return False


    # NOTE: Used for continuously calculating average embedding. Keeping out of curiosity.
    # def average_embedding(self, name, embedding):
    #     import ast
    #     with self.conn.cursor() as cursor:
    #         # Start a transaction explicitly
    #         cursor.execute("BEGIN;")
    #
    #         # Get the current data from the table
    #         cursor.execute(
    #             """
    #             SELECT embedding, embedding_count
    #             FROM embeddings
    #             WHERE name = %s;
    #             """,
    #             (name,)
    #         )
    #         current_data = cursor.fetchone()
    #
    #         if current_data:
    #             average_embedding, embedding_count = current_data
    #
    #             # TODO: This is a terrible hack. Clean up type guessing
    #             # Ensure both `average_embedding` and `embedding` are lists of floats
    #             try:
    #                 # Convert string to a list (if it's stored as a string)
    #                 if isinstance(average_embedding, str):
    #                     average_embedding = ast.literal_eval(average_embedding)
    #
    #                 if not isinstance(average_embedding, list):
    #                     raise ValueError("average_embedding must be a list.")
    #
    #                 # Ensure embedding is a list of floats
    #                 if not isinstance(embedding, list):
    #                     embedding = [float(emb) for emb in embedding]
    #
    #                 # Calculate the new average and embedding count
    #                 new_average_embedding = [
    #                     (embedding_count * avg + emb) / (embedding_count + 1)
    #                     for avg, emb in zip(average_embedding, embedding)
    #                 ]
    #                 new_embedding_count = embedding_count + 1
    #                 # Update the table with the new values
    #                 cursor.execute(
    #                     """
    #                     UPDATE embeddings
    #                     SET embedding = %s,
    #                         embedding_count = %s
    #                     WHERE name = %s;
    #                     """,
    #                     (new_average_embedding, new_embedding_count, name)
    #                 )
    #             except Exception as e:
    #                 print(f"Error: {e}")
    #
    #         # Commit the transaction
    #         self.conn.commit()

