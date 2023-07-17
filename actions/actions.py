import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils import DB


class ActionSelectRandomTopic(Action):

    def name(self) -> Text:
        return "action_select_random_topic"

    def get_random_topic(self, level: str, exclude: list) -> str:
        """"""

        topics = [
            item for item in DB.get_topics(level) 
            if item not in exclude
        ]

        return random.choice(topics)

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
        ) -> List[Dict[Text, Any]]:

        level = tracker.get_slot("level")
        topic = tracker.get_slot("topic")

        new_topic = self.get_random_topic(level, [topic])

        return [SlotSet("topic", new_topic)]

class ActionSelectRandomWords(Action):

    def name(self) -> Text:
        return "action_select_random_word"

    def get_random_word(self, level: str, topic: str, exclude: list) -> str:
        """"""

        words = [
            item for item in DB.get_words(level, topic) 
            if item not in exclude
        ]

        return random.choice(words)

    def run(
            self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
        ) -> List[Dict[Text, Any]]:

        level = tracker.get_slot("level")
        topic = tracker.get_slot("topic")
        word = tracker.get_slot("word")

        new_word = self.get_random_word(level, topic, [word])

        return [SlotSet("word", new_word)]
    

class GenerateAnswer(Action):

    def name(self) -> Text:
        return "action_ask_finish_game"

    def build_prompt(self, mode: str, level: str, word: str):
        pass

    def retrieve_context(self) -> List[Dict[Text, Text]]:
        pass

    def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
        ) -> List:
        
        dispatcher.utter_message(
            response="utter_llm_output",
            text="LLM output"
        )

        return []
    
class ValidateRestaurantForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_game_form"

    async def extract_finish_game(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:

        # retrieve value from mapping conditions
        slot_value = tracker.get_slot("finish_game")
        
        if False:
            # check if user win game
            return {"finish_game": True}

        return {"finish_game": slot_value}
    
    async def validate_finish_game(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value is True:
            return {"finish_game": slot_value} # finish game
        else:
            return {"finish_game": None} # continue game