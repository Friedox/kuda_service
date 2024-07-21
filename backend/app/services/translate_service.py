import re

from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')

non_english_pattern = re.compile(r'[^\x00-\x7F]+')


def translate(text: str) -> str:
    if non_english_pattern.search(string=text):
        return translator.translate(text=text)
    return text

