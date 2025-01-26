import argparse
import shlex
from .facer import Facer

from loguru import logger
import sys

logger.remove()

def setup_logger(verbose: bool):
    logger.add(sys.stdout, level="DEBUG" if verbose else "INFO")


def build_parser():
    parser = argparse.ArgumentParser(description="Detect and recognize face with deepface")
    subparsers = parser.add_subparsers(dest="command")

    insert_parser = subparsers.add_parser("insert", help="Insert the retrieved embedding")
    insert_parser.add_argument("input", help="Input image path")
    insert_parser.add_argument("name", help="Name of person in image")
    insert_parser.add_argument('-v', "--verbose", action='store_true', help='Display debug logs')

    check_parser = subparsers.add_parser("match", help="Match the retrieved embedding")
    check_parser.add_argument("input", help="Input image path")
    check_parser.add_argument('-v', "--verbose", action='store_true', help='Display debug logs')

    return parser

def command_dispatcher(args, facer):
    setup_logger(args.verbose)

    try:
        if args.command == "insert":
            facer.insert(args.name, args.input)
        elif args.command == "match":
            facer.match(args.input)
        else:
            logger.error(f"Unknown command: {args.command}")
    except Exception as e:
        logger.exception(f"Error executin command: {args.command}")

def interactive_prompt(parser, facer):
    print("Enter 'help' for available commands or 'exit' to quit.")

    while True:
        try:
            user_input = input("Facer >>> ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("Closing facer")
                break

            if user_input.lower() in ["help", "--help"]:
                parser.print_help()
                continue

            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                continue
            command_dispatcher(args, facer)
        except Exception as e:
                logger.exception("An error occurred: {}", e)

def main():
    parser = build_parser()
    facer = Facer()

    if len(sys.argv) > 1:
        args = parser.parse_args()
        command_dispatcher(args, facer)
    else:
        interactive_prompt(parser, facer)

    facer.db.close()

