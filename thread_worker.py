import threading

import spacy
import constant


class ThreadWorker(threading.Thread):

    def __init__(self, thread_id, output_directory, poll_work_callback):
        threading.Thread.__init__(self)
        self._id = thread_id
        self._output_directory = output_directory
        self._poll_work_callback = poll_work_callback
        self._nlp = ThreadWorker._load_spacy()

    def run(self):
        input_file = self._poll_next_work_item()
        while input_file:
            self._process_file(input_file)
            input_file = self._poll_next_work_item()

    def _poll_next_work_item(self):
        input_file = self._poll_work_callback()
        if not input_file or not input_file.is_file():
            return None
        return input_file

    @staticmethod
    def _load_spacy():
        return spacy.load("en_core_web_sm")

    @staticmethod
    def _replace_entities(doc):
        text = list(doc.text)
        for person in ThreadWorker._entities(doc):
            person_without_space = person.text.replace(" ", "_")
            for x in range(person.start_char, person.end_char):
                text[x] = person_without_space[x - person.start_char]

        return "".join(text)

    @staticmethod
    def _entities(doc):
        entities = []
        for entity in doc.ents:
            if not ThreadWorker._is_entity(entity):
                continue

            entities.append(entity)
        return entities

    @staticmethod
    def _is_entity(entity):
        return entity.label_ in constant.ENTITY_LABELS

    def _process_file(self, input_file):
        with input_file.open() as file, open(f"{self._output_directory}{input_file.name}", "w+", buffering=512000) as output:
            doc = self._nlp(file.read())
            print(f"{ThreadWorker._replace_entities(doc)}", file=output, end="")
