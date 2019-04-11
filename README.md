# Spacy NER

This script converts a text consisting of plain words (separated by white space) in a text consisting of phrases.
Phrases might be just ordinary words as in the beginning, but more importantly, they might be named entities as recognized by SpaCy.
Those phrases may consist of multiple plain words, which are afterwards merged into one word using underscores.

```
Example: New York City -> New_York_City
```

## Usage

```sh
python3 spacy_ner.py --input={PATH_TO_CLEANED_TEXT} --output={PATH_TO_OUTPUT=stdout}
```
