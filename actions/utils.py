import os
import json
import openai


END_OF_GAME_MARKER = "@COMPLETED"


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

class PromptBuilder:

    def __init__(self, prompts: dict) -> "PromptBuilder":
        self.prompts = prompts
        super().__init__()

    @staticmethod
    def from_file(path: str) -> "PromptBuilder":
        with open(path) as f:
            prompts = json.load(f)

        return PromptBuilder(prompts)

    @staticmethod
    def from_dict(object: dict) -> "PromptBuilder":
        return PromptBuilder(object)
    
    def get_prompt(self, game_mode: str) -> str:
        return self.prompts[game_mode]

    def set_params(self, prompt: str, **params) -> str:
        for k, v in params.items():
            prompt = prompt.replace(f"{{{k}}}", v)
        return prompt

    def __call__(self, game_mode: str, level: str, word: str) -> str:
        prompt = self.get_prompt(game_mode)
        prompt = self.set_params(prompt, level=level, word=word)

        return prompt

class LLMRunner:
    def __call__(self, messages: list) -> str:
        ...

class OpenaiRunner(LLMRunner):
    def __init__(self, model: str):
        self.model = model

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_base = os.environ.get("OPENAI_API_BASE")

    def __call__(self, messages: list) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=80
        )

        return response.choices[0].message["content"]


_debug_db = {
    "beginner": {
        "topic_a": ["w_a1", "w_a2"],
        "topic_b": ["w_b1", "w_b2"],
    },
    "advanced": {
        "topic_c": ["w_c1", "w_c2"],
        "topic_d": ["w_d1", "w_d2"],
    },
}

_debug_prompts = {
    "guess": """
prompt mode=guess word={word} level={level}
""",
    "explain": """
prompt mode=explain word={word} level={level}
"""
}

database = JsonDatabase.from_dict(_debug_db)
prompt_builder = PromptBuilder.from_dict(_debug_prompts)
openai_runner = OpenaiRunner(model="gpt-3.5-turbo")