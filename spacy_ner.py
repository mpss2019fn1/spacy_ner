import argparse
import sys
import os
import spacy

from accessible_file import AccessibleFile

entity_labels = [u"PERSON", u"FAC", u"ORG", u"GPE", u"LOC", u"WORK_OF_ART"]


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    output = args.output
    if output:
        output = open(output, "w")
    else:
        output = sys.stdout

    nlp = spacy.load("en_core_web_sm")
    input_path = os.path.abspath(os.path.expanduser(args.input))
    with open(input_path) as input_file:
        current_line = 0
        for line in input_file:
            doc = nlp(line)
            print(f"{_replace_entities(doc)}", file=output, end="")
            current_line += 1


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input file location", action=AccessibleFile)
    parser.add_argument("--output", help="output file location")

    return parser


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
