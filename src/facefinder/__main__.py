import argparse
from .analyze import detect_face, get_embedding
from .postgresql_client import insert_embedding, check_embedding

def main():
    parser = argparse.ArgumentParser(
        description="Detect and recognize face with deepface"
    )

    parser.add_argument("-i", "--input", required=True, help="Input image")
    # parser.add_argument(
    #     "-o", "--output", default="output.png", type=str, help="Output folder"
    # )
    parser.add_argument(
        "--embedding", action="store_true", help="Converting folder of images to faces"
    )
    parser.add_argument(
        "--insert", action="store_true", help="Insert the retrieved embedding"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check the retrieved embedding"
    )

    args = parser.parse_args()

    # TODO: Check if unnecessary flags are set: Both insert and check should not be set to true

    if args.embedding:
        embedding = get_embedding(args.input)
        if args.insert:
            insert_embedding("test", embedding)
        elif args.check:
            result = check_embedding(embedding)
            print(f"Result: {result}")
    else:
        detect_face(args.input)



