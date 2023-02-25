import genanki
import logging
from collections import namedtuple
logger = logging.getLogger("general")


class Entry:
    def __init__(self, word, category, entry):
        self.category = category
        self._entry = entry
        self._word = word
        self.senses: list[Sense] = [Sense(d) for d in self.entry["senses"]]

    def is_informal(self):
        for r in self.entry.get("registers", []):
            if r["id"] == "informal":
                return True
        return False

    def has_too_many_senses(self):
        if len(self.entry["senses"]) > 5:
            return False
        return True

    @property
    def word(self):
        return self._word

    @property
    def media(self):
        for d in self.entry["pronunciations"]:
            if "audioFile" in d:
                return d["audioFile"]
        return None

    @property
    def pronunciation(self):
        for d in self.entry["pronunciations"]:
            if d.get("phoneticNotation", "") == "IPA":
                return d["phoneticSpelling"]
        return None

    def get_other_definitions(self, sense):
        other_definitions = [s.definition for s in self.senses if s is not sense]
        return other_definitions


class Sense:
    def __init__(self, data):
        self.data = data

    @property
    def definition(self):
        return "\n".join(self.data["definitions"])

    @property
    def example(self):
        return self.data["examples"][0]

    @property
    def synonyms(self):
        return [d["text"] for d in self.data["synonyms"]]


Note = namedtuple("Note", [
    "word",
    "media",
    "pronunciation",
    "definition",
    "example",
    "orther_definitions",
    "category",
    "synonyms",
    "comment"
])


class Extractor:
    rules = [
        "is_informal",
        "has_too_many_senses"
    ]

    def __init__(self, result):
        import pdb;pdb.set_trace()
        lexical_entries = result["results"][0]["lexicalEntries"]
        self.word = result["id"]
        self.entries = [
            Entry(self.word, lexical_entry["lexicalCategory"]["id"], entry)
            for lexical_entry in lexical_entries
            for entry in lexical_entry["entries"]
        ]

    def check_rules(self, e):
        for name in self.rules:
            if getattr(e, name)():
                return name
        return None

    def process(self) -> list[Entry]:
        formal_entries = []
        for e in self.entries:
            rule_name = self.check_rules(e)
            if rule_name:
                logger.info(f"ignore {e.word} because of {rule_name}")
            else:
                formal_entries.append(e)
        return formal_entries


class Anki:
    def __init__(self):
        self.model_name = "English Model"
        self.model = genanki.Model(
            hash(self.model_name),
            self.model_name,
            fields=[{"name": f} for f in Note._fields],
            templates=[dict((f, "{{" + f + "}}") for f in Note._fields)]
        )

        self.deck = genanki.Deck(
                hash("English"),
                'English'
        )

    def add_note(self, note: Note):
        anki_note = genanki.Note(model=Anki, fields=note)
        self.deck.add_note(anki_note)

    def add_entry(self, entry: Entry):
        for sense in entry.senses:
            note = Note(
                entry.word,
                entry.media,
                entry.pronunciation,
                sense.definition,
                sense.example,
                "\n".join(entry.get_other_definitions(sense)),
                entry.category,
                "\n".join(sense.synonyms),
                ""
            )
            self.add_note(note)

    def add_words(self, words: dict):
        for word_id, data in words.items():
            entries = Extractor(data).process()
            for entry in entries:
                self.add_entry(entry)

    def generate(self):
        deck = genanki.Package(self.deck)

        deck.write_to_file('output.apkg')
