import random

from json import loads

from src.config import Config


class IntentRepository:
    def __init__(self):
        self.__intents = loads(
            open(f'{Config.basedir}/src/static/models/intents.json').read()
            .replace('BOT', Config.bot)
            .replace('CONSTRUCTOR', Config.constructor)
            .replace('HOMEPAGE', Config.homepage)
            .replace('CONTACT', Config.contact)
            .replace('AGE', Config.age)
        )

    @property
    def intents(self):
        return self.__intents

    def find_all_intents(self):
        return [intent for intent in self.intents['intents']]

    def find_all_intent_contexts_group_by_intent(self):
        return [intent['context'] for intent in self.intents['intents'] if 'context' in intent]

    def find_all_intent_patterns_group_by_intent(self):
        return [intent['patterns'] for intent in self.intents['intents'] if 'patterns' in intent]

    def find_all_intent_patterns(self):
        return [pattern for intent in self.intents['intents'] for pattern in intent['patterns']]

    def find_intents_by_pattern(self, pattern):
        patterns = self.find_all_intent_patterns_group_by_intent()
        tags_index = [index for index, pattern_group in enumerate(patterns) if any(p in pattern for p in pattern_group)]
        return [self.intents['intents'][index] for index in tags_index if len(tags_index) > 0] if len(
                tags_index) > 0 else []

    def find_intents_by_tag(self, tag):
        return [intent for intent in self.intents['intents'] if tag == intent['tag']]

    def find_one_intent_response_by_tag_order_by_random(self, tag):
        first_intent = self.find_intents_by_tag(tag)[0]
        return random.choice(first_intent['responses'])

    def find_intent_tags_by_pattern(self, pattern):
        intents = self.find_intents_by_pattern(pattern)[0]
        return [{'intent': intent['tag']} for intent in intents]
