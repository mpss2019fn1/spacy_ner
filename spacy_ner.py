import argparse
import sys
import os
import spacy

from validate_file import ValidateFile
from validate_directory import ValidateDirectory

entity_labels = [u"PERSON", u"FAC", u"ORG", u"GPE", u"LOC", u"WORK_OF_ART"]


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    if "action" not in args or not args.action:
        parser.print_usage()
        return

    if args.action == "file":
        _action_file(args)
        return

    if args.action == "dir":
        _action_dir(args)
        return

    parser.print_usage()


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _create_file_parser(subparsers)
    _create_dir_parser(subparsers)
    return parser


def _create_file_parser(subparsers):
    file_parser = subparsers.add_parser("file", description="parses *one* big input file")
    file_parser.set_defaults(action="file")
    file_parser.add_argument("--input", required=True, help="input file location", action=ValidateFile)
    file_parser.add_argument("--output", help="output file location")


def _create_dir_parser(subparsers):
    dir_parser = subparsers.add_parser("dir", description="parses multiple files within a given directory")
    dir_parser.set_defaults(action="dir")
    dir_parser.add_argument("--source", required=True, help="directory, which contains the files", action=ValidateDirectory)
    dir_parser.add_argument("--target", required=True, help="directory, which will contain the output files", action=ValidateDirectory)


def _action_file(args):
    output = args.output
    if output:
        output = open(output, "w")
    else:
        output = sys.stdout

    nlp = _load_spacy()
    input_path = os.path.abspath(os.path.expanduser(args.input))
    with open(input_path) as input_file:
        for line in input_file:
            doc = nlp(line)
            print(f"{_replace_entities(doc)}", file=output, end="")


def _action_dir(args):
    nlp = _load_spacy()
    for filename in os.listdir(args.source):
        with open(f"{args.source}/{filename}", "r") as input_file, open(f"{args.target}/{filename}", "w+") as output_file:
            for line in input_file:
                doc = nlp(line)
                print(f"{_replace_entities(doc)}", file=output_file, end="")


def _load_spacy():
    return spacy.load("en_core_web_sm")


def _replace_entities(doc):
    text = list(doc.text)
    for person in _entities(doc):
        person_without_space = person.text.replace(" ", "_")
        for x in range(person.start_char, person.end_char):
            text[x] = person_without_space[x - person.start_char]

    return "".join(text)


def _entities(doc):
    entities = []
    for entity in doc.ents:
        if not _is_entity(entity):
            continue

        entities.append(entity)
    return entities


def _is_entity(entity):
    return entity.label_ in entity_labels


if __name__ == "__main__":
    main()
