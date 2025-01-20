import argparse
import shlex
# from deepface import DeepFace
from .analyze import detect_face, get_embedding
from .postgresql_client import EmbeddingDatabase

db = EmbeddingDatabase()

def interactive_prompt():
    parser = build_parser()

    while True:
        user_input = input("FaceFinder>>> ").strip()
        if user_input.lower() == "exit":
            print("Closing facefinder")
            break
        elif user_input.lower() == "help" or user_input == "--help":
            parser.print_help()
        else:
            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                continue
            command_dispatcher(args)

    db.close()

def build_parser():
    parser = argparse.ArgumentParser(
        description="Detect and recognize face with deepface"
    )

    parser.add_argument("-i", "--input", help="Input image")
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
    return parser

def command_dispatcher(args):
    # TODO: Check if unnecessary flags are set: Both insert and check should not be set to true
    if args.embedding:
        # TODO: Only run this if the command is valid: If nothing set for --insert then it will error but embedding will run
        embedding = get_embedding(args.input)
        if args.insert:
            db.insert_embedding(args.insert, embedding)
        elif args.check:
            result = db.check_embedding(embedding)
            print(f"Result: {result}")
        else:
            # TODO: This never gets called because --insert expects a value
            print("No action for embedding specified")
    else:
        detect_face(args.input)


def main():
    parser = build_parser()

    args = parser.parse_args()
    command_dispatcher(args)
    db.close()



