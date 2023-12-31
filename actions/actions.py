import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict

from actions.utils import (
    vocab_database, 
    prompt_builder, 
    openai_runner
)


class ActionSelectRandomTopic(Action):
    """selects word by given level"""

    def name(self) -> Text:
        return "action_select_random_topic"

    def get_random_topic(self, level: str, exclude: list) -> str:
        """"""

        topics = [
            item for item in vocab_database.get_topics(level) 
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
    """selects word by given level and topic"""

    def name(self) -> Text:
        return "action_select_random_word"

    def get_random_word(self, level: str, topic: str, exclude: list) -> str:
        """"""

        words = [
            item for item in vocab_database.get_words(level, topic) 
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

class ActionBeginOfTheGame(Action):
    """sets game_status to None"""

    def name(self) -> Text:
        return "action_begin_of_the_game"
    
    def run(self, dispatcher, tracker, domain) -> List:
        return [SlotSet("game_status", None)]

class ActionAskGameStatus(Action):
    """fake action, actual response comes from validation action"""

    def name(self) -> Text:
        return "action_ask_game_status"
    
    def run(self, dispatcher, tracker, domain) -> List:
        return []
    
class ValidateGameForm(FormValidationAction):
    """checks if game_status completed and sends teacher response"""

    def name(self) -> Text:
        return "validate_game_form"

    def get_teacher_response(self, tracker: Tracker) -> Text:
        """"""

        prompt = self.get_prompt(tracker)
        context = self.get_context(tracker)

        messages = [{"role": "system", "content": prompt}]
        messages = messages + context

        return openai_runner(messages)
    
    def get_prompt(self, tracker: Tracker) -> Text:
        """"""
        
        return prompt_builder(
            game_mode=tracker.get_slot("game_mode"),
            topic=tracker.get_slot("topic"),
            level=tracker.get_slot("level"),
            word=tracker.get_slot("word")
        )

    def get_context(self, tracker: Tracker) -> List[Dict[Text, Text]]:
        """retrievs bot/user messages just after action_begin_of_the_game"""

        events = tracker.events_after_latest_restart()

        for idx in range(len(events) - 1, -1, -1):
            if (
                events[idx]["event"] == "action" and
                events[idx]["name"] == "action_begin_of_the_game"
            ):
                break
        
        messages = []
        for item in events[idx+1:]:
            if item["event"] in ["user", "bot"]:
                text: str = item["text"]

                if item["event"] == "user":
                    role = "user"
                else:
                    role = "assistant"
                    text = text.replace("Bob: ", "")

                messages.append({
                    "role": role, 
                    "content": text
                })

        return messages

    def is_game_completed(self, tracker: Tracker, last_bot_message: str) -> bool:
        """checks if target word was messaged by user/bot"""

        context = self.get_context(tracker)
        
        messages = [c["content"] for c in context] + [last_bot_message]

        word: str = tracker.get_slot("word")
        for m in reversed(messages):
            if word.lower() in m.lower():
                return True

        return False

    async def extract_game_status(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:

        slot_value = None
        response_template = "utter_teacher_response"

        # use dialog context to generate next response
        response_text = self.get_teacher_response(tracker)

        # check if context has any markers of completed game
        if self.is_game_completed(tracker, response_text):
            # when bot correctly names target word in `explain` mode
            # use predefined template to inform user and give feedback
            if tracker.get_slot("game_mode") == "explain":
                response_text = tracker.get_slot("word")
                response_template = "utter_correct_word"
            
            # mark this game as completed
            slot_value = "completed"
        
        # actual ask for game_status slot
        dispatcher.utter_message(
            response=response_template,
            payload=response_text
        )
        
        return {"game_status": slot_value}
    
    def validate_game_status(self, slot_value, dispatcher, tracker, domain) -> Dict[Text, Any]:
        """just returns same value to turn of warnings"""

        return {"game_status": slot_value}