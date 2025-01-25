import argparse
import shlex
from .facer import Facer


def interactive_prompt():
    parser = build_parser()
    facer = Facer()

    while True:
        user_input = input("Facer >>> ").strip()
        if user_input.lower() == "exit":
            print("Closing facer")
            break
        elif user_input.lower() == "help" or user_input == "--help":
            parser.print_help()
        else:
            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                continue
            command_dispatcher(args, facer)
    facer.db.close()

def build_parser():
    parser = argparse.ArgumentParser(description="Detect and recognize face with deepface")
    subparsers = parser.add_subparsers(dest="command")

    insert_parser = subparsers.add_parser("insert", help="Insert the retrieved embedding")
    insert_parser.add_argument("input", help="Input image path")
    insert_parser.add_argument("name", help="Name of person in image")

    check_parser = subparsers.add_parser("match", help="Match the retrieved embedding")
    check_parser.add_argument("input", help="Input image path")

    return parser

def command_dispatcher(args, facer):
    if args.command == "insert":
        facer.insert(args.name, args.input)
    elif args.command == "match":
        facer.match(args.input)
    else:
        print("This shouldn't happen")
        # print("Running default detect_face")
        # detect_face(args.input)


def main():
    parser = build_parser()

    args = parser.parse_args()
    facer = Facer()
    command_dispatcher(args, facer)
    facer.db.close()



