import json


def load_language(lang: str = 'en') -> dict:
    with open('data/language/{}.json'.format(lang), "r") as read_file:
        dict_lang = json.load(read_file)
    return dict_lang
