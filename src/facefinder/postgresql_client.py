import psycopg
from dotenv import load_dotenv
import numpy as np
import os
# from pgvector.psycopg import register_vector

load_dotenv()

def insert_embedding(name, embedding):

    connection_string = f"postgres://{os.getenv('USER')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    print(connection_string)
    embedding = np.array(embedding)

    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO embeddings (name, embedding) VALUES (%s, %s)",
                (name, embedding.tolist(),)
            )
            conn.commit()

def check_embedding(embedding):
    connection_string = f"postgres://{os.getenv('USER')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    print(connection_string)
    embedding = np.array(embedding)
    with psycopg.connect(connection_string) as conn:
        # conn.execute('CREATE EXTENSION IF NOT EXISTS vector') # TODO: Check if this is necessary
        # register_vector(conn) # TODO: Also check if this is necessary
        with conn.cursor() as cursor:
            result = conn.execute('SELECT name, (embedding <-> %s::vector) AS euclidean_distance FROM embeddings ORDER BY euclidean_distance LIMIT 5', (embedding.tolist(),)).fetchall()

    return result

