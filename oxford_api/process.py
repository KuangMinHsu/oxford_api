import logging
from .api import ParallelAPI
from .store import Storage
from .anki import Anki

logger = logging.getLogger("general")


def read_input(filename):
    text = open(filename).read()
    return text.strip().split("\n")


def normalize(vocabularies):
    return set(v.lower() for v in vocabularies)


def process(filename):
    vocabularies = read_input(filename)
    word_ids = normalize(vocabularies)
    storage = Storage()
    api = ParallelAPI()
    known_words = storage.get(word_ids)
    word_ids = word_ids - set(known_words.keys())
    rets, errors = api.entries(word_ids)
    print(f"query {len(rets)} successfully")
    print(f"query {len(rets)} unsuccessfully")
    if errors:
        logger.error(errors)
    storage.upsert_many(rets)
    known_words.update(rets)
    anki = Anki()
    anki.add_words(known_words)
    anki.generate()
