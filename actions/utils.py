import json


class Database:
    def get_topics(self, level: str) -> list[str]:
        ...
    
    def get_words(self, level: str, topic: str) -> list[str]:
        ...

class JsonDatabase(Database):
    """
    {
        "level_1": {
            "topic_a": ["w_a1", "w_a2", ...],
            "topic_b": ["w_b1", "w_b2", ...],
            ...
        },
        "level_2": {
            "topic_c": ["w_c1", "w_c2", ...],
            ...
        },
        ...
    }
    """

    def __init__(self, db: dict) -> "JsonDatabase":
        self.db = db
        super().__init__()

    @staticmethod
    def from_file(path: str) -> "JsonDatabase":
        with open(path) as f:
            db = json.load(f)

        return JsonDatabase(db)

    @staticmethod
    def from_dict(object: dict) -> "JsonDatabase":
        return JsonDatabase(object)
    
    def get_topics(self, level: str) -> list[str]:
        topic_to_words: dict = self.db[level]
        return list(topic_to_words.keys())

    def get_words(self, level: str, topic: str) -> list[str]:
        topic_to_words: dict = self.db[level]
        return topic_to_words[topic]

_debug = {
    "beginner": {
        "topic_a": ["w_a1", "w_a2"],
        "topic_b": ["w_b1", "w_b2"],
    },
    "advanced": {
        "topic_c": ["w_c1", "w_c2"],
        "topic_d": ["w_d1", "w_d2"],
    },
}

DB = JsonDatabase.from_dict(_debug)