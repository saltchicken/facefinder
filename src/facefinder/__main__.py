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
        "--insert", default=None, help="Insert the retrieved embedding"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check the retrieved embedding"
    )

    args = parser.parse_args()

    # TODO: Check if unnecessary flags are set: Both insert and check should not be set to true

    if args.embedding:
        # TODO: Only run this if the command is valid: If nothing set for --insert then it will error but embedding will run
        embedding = get_embedding(args.input)
        if args.insert:
            insert_embedding(args.insert, embedding)
        elif args.check:
            result = check_embedding(embedding)
            print(f"Result: {result}")
        else:
            # TODO: This never gets called because --insert expects a value
            print("No action for embedding specified")
    else:
        detect_face(args.input)



