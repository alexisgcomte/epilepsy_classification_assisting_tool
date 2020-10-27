from epilepsy_classification_assisting_tool.loading.loading import (
    simplified_key_words)
import pandas as pd


def test_hello():
    a = 'hello'
    assert a == 'hello'

def test_loading_simplified_key_words_output_list():
    target_tags_list, correspondance_dataset = simplified_key_words()
    assert type(target_tags_list) == list 

def test_loading_simplified_key_words_output_DataFrame():
    target_tags_list, correspondance_dataset = simplified_key_words()
    assert type(correspondance_dataset) == pd.DataFrame 
