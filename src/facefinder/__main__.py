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
    parser = argparse.ArgumentParser(description="Detect and recognize face with deepface")
    subparsers = parser.add_subparsers(dest="command")

    insert_parser = subparsers.add_parser("insert", help="Insert the retrieved embedding")
    insert_parser.add_argument("input", help="Input image path")
    insert_parser.add_argument("name", help="Name of person in image")

    check_parser = subparsers.add_parser("match", help="Match the retrieved embedding")
    check_parser.add_argument("input", help="Input image path")

    return parser

def command_dispatcher(args):
    if args.command == "insert":
        embedding = get_embedding(args.input)
        # result = db.does_name_exist(args.name)
        # print(f"Result: {result}")
        db.insert_embedding(args.name, embedding)
    elif args.command == "match":
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



