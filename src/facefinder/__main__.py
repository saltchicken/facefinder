import argparse
import shlex
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
        "--insert", default=None, help="Insert the retrieved embedding"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check the retrieved embedding"
    )
    return parser

def command_dispatcher(args):
    if args.insert:
        embedding = get_embedding(args.input)
        db.insert_embedding(args.insert, embedding)
    elif args.check:
        embedding = get_embedding(args.input)
        result = db.check_embedding(embedding)
        print(f"Result: {result}")
    else:
        print("Running default detect_face")
        detect_face(args.input)


def main():
    parser = build_parser()

    args = parser.parse_args()
    command_dispatcher(args)
    db.close()



